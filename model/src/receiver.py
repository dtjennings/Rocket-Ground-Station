#----------------------------------------------------------
# This script contains the python prototype for the LoRa receiver.
#
# The purpose of implementing in Python first was to help me understand 
# what is required to receive complex IQ samples from an SDR and to 
# then retrieve the wanted LoRa telemetry.
#
#----------------------------------------------------------

#----------------------------------------------------------
# Libraries
#----------------------------------------------------------

from pathlib import Path
import numpy as np
import argparse
import json

#----------------------------------------------------------
# Receiver Configurations
#----------------------------------------------------------

receiver_config = {
    "sample_rate": 2.56e6,
    "rf_frequency": 868.1e6,
    "sdr_center_frequency": 868.35e6,
    "bandwidth": 125e3,
    "spreading_factor": 7,
    "power_window_ms": 0.2,
    "detector_margin_db": 6,
    "detector_sigma": 5,
    "detector_hysteresis_db": 2,
    "detector_min_on_ms": 0.4,
    "detector_min_off_ms": 0.6,
    "detector_min_packet_ms": 2,
    "packet_padding_ms": 2.5
}

#----------------------------------------------------------
# Status Functions
#----------------------------------------------------------

def display_info(info, data):
    print(f"[INFO] {info}: {data}")

def display_debug(info, data):
    print(f"[DEBUG] {info}: {data}")
    
def display_error(info, data):
    print(f"[ERROR] {info}: {data}")
    
        
#----------------------------------------------------------
# Data Movement Functions
#----------------------------------------------------------

def load_iq_samples(path):
    
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    
    if path.suffix == ".npy":
        samples = np.load(path)
        display_debug("Array Type", samples.dtype)
        display_debug("Array Shape", samples.shape)
    else:
        raise ValueError("[ERROR] File format must be: .npy")
    
    if samples.size == 0:
        raise ValueError("[ERROR] IQ capture is empty")
    
    return samples

def update_config(path, config):
    
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    config.update(data)
    return


#----------------------------------------------------------
# DSP Functions
#---------------------------------------------------------- 

def covert_to_db(x):
    return 10 * np.log10(np.maximum(x, 1e-15))

def detect_packet_boundaries(iq_samples):
    
    # Calculate average power in short windows
    win = max(8, int(round(receiver_config["power_window_ms"] * 1e-3 * receiver_config["sample_rate"])))
    n_blocks = len(iq_samples) // win
    
    trimmed = iq_samples[: n_blocks * win]
    power = np.mean(np.abs(trimmed.reshape(n_blocks, win)) ** 2, axis=1)
    power_db = covert_to_db(power)

    # Estimate noise from low power windows
    k_noise = max(4, int(np.ceil(0.2 * len(power_db))))
    lower = np.partition(power_db, k_noise - 1)[:k_noise]
    noise_db = float(np.median(lower))
    median_deviation = float(np.median(np.abs(lower - noise_db)))
    robust_sigma_db = max(0.05, 1.4826 * median_deviation)
    margin = max(receiver_config["detector_margin_db"], receiver_config["detector_sigma"] * robust_sigma_db)
    threshold_on = noise_db + margin
    threshold_off = threshold_on - receiver_config["detector_hysteresis_db"]
    
    min_time_on = max(1, int(np.ceil(receiver_config["detector_min_on_ms"] / receiver_config["power_window_ms"])))
    min_time_off = max(1, int(np.ceil(receiver_config["detector_min_off_ms"] / receiver_config["power_window_ms"])))
    
    segments = []
    active = False
    on_count = 0
    off_count = 0
    seg_start = 0
    
    for i, val in enumerate(power_db):
        if not active:
            if val >= threshold_on:
                seg_start = i - min_time_on + 1
                active = True
                off_count = 0
            else:
                on_count = 0
        else:
            if val < threshold_off:
                off_count += 1
                if off_count >= min_time_off:
                    seg_end = i - min_time_off + 1
                    segments.append((seg_start, max(seg_start + 1, seg_end)))
                    active = False
                    on_count = 0
                    off_count = 0
            else:
                off_count = 0
                
    if active:
        segments.append((seg_start, n_blocks))
        
    min_blocks = max(1, int(np.ceil(receiver_config["detector_min_packet_ms"] / receiver_config["power_window_ms"])))
    segments = [s for s in segments if (s[1] - s[0]) >= min_blocks]
    
    if not segments:
        packet_detection_result = {
            "detected": False,
            "start_sample": 0,
            "end_sample": 0,
            "padded_start_sample": 0,
            "padded_end_sample": len(iq_samples),
            "duration_ms": 0,
            "window_samples": win,
            "power_sample_indices": np.arange(n_blocks) * win + win // 2,
            "power_db": power_db,
            "noise_db": noise_db,
            "threshold_on_db": threshold_on,
            "threshold_off_db": threshold_off            
        }
        return packet_detection_result
    
    def segment_score(seg):
        a,b = seg
        return float(np.sum(np.maximum(0.0, power_db[a:b] - noise_db)))
    
    a_block, b_block = max(segments, key=segment_score)
    start = int(a_block * win)
    end = int(min(len(iq_samples), b_block * win))
    pad = int(round(receiver_config["packet_padding_ms"] * 1e-3 * receiver_config["sample_rate"]))
    pstart = max(0, start - pad)
    pend = min(len(iq_samples), end + pad)
    
    packet_detection_result = {
        "detected": True,
        "start_sample": start,
        "end_sample": end,
        "padded_start_sample": pstart,
        "padded_end_sample": pend,
        "duration_ms": (end - start) / receiver_config["sample_rate"] * 1e3,
        "window_samples": win,
        "power_sample_indices": np.arange(n_blocks) * win + win // 2,
        "power_db": power_db,
        "noise_db": noise_db,
        "threshold_on_db": threshold_on,
        "threshold_off_db": threshold_off
    }
    return packet_detection_result

def nominal_frequency_offset():
    return receiver_config["rf_frequency"] - receiver_config["sdr_center_frequency"]

def shift_to_baseband(iq_samples, start_sample_index):
    
    frequency_offset_hz = nominal_frequency_offset()
    
    sample_indices = np.arange(len(iq_samples), dtype=np.float64) + float(start_sample_index)
    local_oscillator = np.exp(-1j * 2.0 * np.pi * frequency_offset_hz * sample_indices / receiver_config["sample_rate"])
    
    return np.asarray(iq_samples) * local_oscillator
    
    
#----------------------------------------------------------
# Receiver Functions
#----------------------------------------------------------

def run_receiver(iq_samples):
    packet = detect_packet_boundaries(iq_samples)
    
    if not packet["detected"]:
        raise RuntimeError("No Packet Detected!")
    
    baseband_iq = shift_to_baseband(iq_samples, 0)
    
    display_info("Baseband IQ Samples", baseband_iq)
    
    
    

#----------------------------------------------------------
# Main
#----------------------------------------------------------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="Existing .npy IQ capture")
    p.add_argument("--config", help="Receiver JSON configuration")
    
    args = p.parse_args()
    display_info("Arguments", args)
    input_path = args.input
    config_path = args.config
    
    display_debug("Input File", input_path)
    iq_samples = load_iq_samples(input_path)
    
    update_config(config_path, receiver_config)
    
    print("-----------------------------------------------")
    print("Receiver Configurations")
    print("-----------------------------------------------\n")
    display_info("Input File", input_path)
    display_info("Sample Rate", receiver_config["sample_rate"])
    display_info("RF frequency", receiver_config["rf_frequency"])
    display_info("SDR Centre Frequency", receiver_config["sdr_center_frequency"])
    display_info("Bandwidth", receiver_config["bandwidth"])
    display_info("Spreading Factor", receiver_config["spreading_factor"])
    
    run_receiver(iq_samples)
    
#----------------------------------------------------------
# Beginning
#----------------------------------------------------------

if __name__ == "__main__":
    main()