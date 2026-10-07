
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np

# Get a list of detected device serial numbers 
serial_numbers = RtlSdr.get_device_serial_addresses()
print(f"[INFO] DEtected Serial Numbers: {serial_numbers}")

try:
    sdr = RtlSdr()
    print("[PASS] RTL-SDR Detected!")
except Exception as e:
    print("[ERROR] No RTL-SDR Detected!")
    
# Configure SDR Parameters
sdr.sample_rate = 2.4e6 # 2.4 MS/s
sdr.center_freq = 869.5e6 # 869.5 MHz
sdr.gain = 9 

##########################################

# Tools to inspect the device
center_freq = sdr.get_center_freq()
print(f"[INFO] Center Frequency: {center_freq / 1e6:.2f} MHz")

freq_correction = sdr.get_freq_correction()
print(f"[INFO] Frequency Correction: {freq_correction}")

sample_rate = sdr.get_sample_rate()
print(f"[INFO] Sample Rate: {sample_rate / 1e6:.2f} MS/s")

bandwidth = sdr.get_bandwidth()
print(f"[INFO] Bandwidth: {bandwidth}")

gain = sdr.get_gain()
print(f"[INFO] Gain: {gain}")

gains = sdr.get_gains()
print(f"[INFO] Gain: {gains}")

tuner_type = sdr.get_tuner_type()
print(f"[INFO] Tuner Type: {tuner_type}")

##########################################

# Investigating samples
samples = sdr.read_samples(1024)

print(f"[INFO] Samples type: {type(samples)}")
print(f"[INFO] Samples shape: {samples.shape}")
print(f"[INFO] Samples dtype: {samples.dtype}")

print(f"[INFO] Sample 0: {samples[0]}")
print(f"[INFO] Sample 1: {samples[1]}")
print(f"[INFO] Sample 2: {samples[2]}")

sdr.close()