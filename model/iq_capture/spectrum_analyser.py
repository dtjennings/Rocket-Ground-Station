
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
    
# Tools to inspect the device
center_freq = sdr.get_center_freq()
print(f"[INFO] Center Frequency: {center_freq}")

freq_correction = sdr.get_freq_correction()
print(f"[INFO] Frequency Correction: {freq_correction}")

sample_rate = sdr.get_sample_rate()
print(f"[INFO] Sample Rate: {sample_rate}")

bandwidth = sdr.get_bandwidth()
print(f"[INFO] Bandwidth: {bandwidth}")

gain = sdr.get_gain()
print(f"[INFO] Gain: {gain}")

gains = sdr.get_gains()
print(f"[INFO] Gain: {gains}")

tuner_type = sdr.get_tuner_type()
print(f"[INFO] Tuner Type: {tuner_type}")

sdr.close()