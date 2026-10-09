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
    "spreading_factor": 7
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
    display_info("Receiver Configurations", receiver_config)
    
    print("-----------------------------------------------")
    print("Receiver Configurations")
    print("-----------------------------------------------\n")
    display_info("Input File", input_path)
    display_info("Sample Rate", receiver_config["sample_rate"])
    display_info("RF frequency", receiver_config["rf_frequency"])
    display_info("SDR Centre Frequency", receiver_config["sdr_center_frequency"])
    display_info("Bandwidth", receiver_config["bandwidth"])
    display_info("Spreading Factor", receiver_config["spreading_factor"])
    
#----------------------------------------------------------
# Beginning
#----------------------------------------------------------

if __name__ == "__main__":
    main()