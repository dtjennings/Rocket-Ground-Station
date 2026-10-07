import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.center_freq = 869.5e6

gains = sdr.get_gains()
print("[INFO] Supported gains:", gains)

min_gain = min(gains) / 10
max_gain = max(gains) / 10
print(f"[INFO] Requested min gain: {min_gain} dB")
print(f"[INFO] Requested max gain: {max_gain} dB")

def avg_power():
    samples = sdr.read_samples(256 * 1024)
    power = np.mean(np.abs(samples) ** 2)
    power_dB = 10 * np.log10(power)
    return power_dB

sdr.set_agc_mode(False)
sdr.gain = min_gain
print(f"[INFO] Actual min gain: {sdr.gain}")

min_gain_powers = []
for i in range(5):
    pow = avg_power()
    min_gain_powers.append(pow)
    
sdr.gain = max_gain
print(f"[INFO] Actual max gain: {sdr.gain}")

# Discard initial samples after changing gain
for i in range(3):
    sdr.read_samples(256 * 1024)

max_gain_powers = []
for i in range(5):
    pow = avg_power()
    max_gain_powers.append(pow)
    
min_avg_power = np.mean(min_gain_powers)
max_avg_power = np.mean(max_gain_powers)
    
print(f"[INFO] Average Power at Min Gain: {min_avg_power:.2f} dB")
print(f"[INFO] Average Power at Max Gain: {max_avg_power:.2f} dB")

sdr.close()
    
