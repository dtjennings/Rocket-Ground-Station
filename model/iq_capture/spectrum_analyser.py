#-----------------------------------------------------------
# The purpose of this program is to help me understand 
# how to collect samples from the rtl-sdr
#-----------------------------------------------------------

import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import numpy as np

# Parameters
N = 256 * 1024
Fs = 2.56e6
fc = 868.1e6

# Get a list of detected device serial numbers 
serial_numbers = RtlSdr.get_device_serial_addresses()
print(f"[INFO] DEtected Serial Numbers: {serial_numbers}")

try:
    sdr = RtlSdr()
    print("[PASS] RTL-SDR Detected!")
except Exception as e:
    print("[ERROR] No RTL-SDR Detected!")
    
# Configure SDR Parameters
sdr.sample_rate = Fs # 2.4 MS/s
sdr.center_freq = fc # 869.5 MHz
sdr.gain = 9 

#-----------------------------------------------------------

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

#-----------------------------------------------------------

# Investigating samples
samples = sdr.read_samples(N)
sdr.close()

print(f"[INFO] Samples type: {type(samples)}")
print(f"[INFO] Samples shape: {samples.shape}")
print(f"[INFO] Samples dtype: {samples.dtype}")

print(f"[INFO] Sample 0: {samples[0]}")
print(f"[INFO] Sample 1: {samples[1]}")
print(f"[INFO] Sample 2: {samples[2]}")

# Seperate the complex IQ into it's real and imaginary components
real_samples = samples.real
imag_samples = samples.imag

print(f"\n[INFO] ### Real Parts ###")
print(f"[INFO] Sample 0: {real_samples[0]}")
print(f"[INFO] Sample 1: {real_samples[1]}")
print(f"[INFO] Sample 2: {real_samples[2]}")

print(f"\n[INFO] ### Imag Parts ###")
print(f"[INFO] Sample 0: {imag_samples[0]}")
print(f"[INFO] Sample 1: {imag_samples[1]}")
print(f"[INFO] Sample 2: {imag_samples[2]}")

#-----------------------------------------------------------

n = np.arange(N)

# Plot I samples
plt.figure()
plt.plot(n, real_samples, label="I")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.show()

# Plot Q samples
plt.figure()
plt.plot(n, imag_samples, label="Q")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.show()

#-----------------------------------------------------------

magnitudes = np.abs(samples)
print(f"[INFO] Magnitude 0: {magnitudes[0]}")
print(f"[INFO] Magnitude 1: {magnitudes[1]}")
print(f"[INFO] Magnitude 2: {magnitudes[2]}")

# Plotting Amplitude vs sample number
plt.figure()
plt.plot(n, magnitudes, label="Magnitudes")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.show()

#-----------------------------------------------------------

fft_bins = np.fft.fft(samples)
fft_bins = np.fft.fftshift(fft_bins)
fft_mag = 10 * np.log10(np.maximum(np.abs(fft_bins), 1e-12))

print(f"[INFO] FFT Samples shape: {fft_bins.shape}")
print(f"[INFO] FFT Samples dtype: {fft_bins.dtype}")

# Plotting FFT magnitude against bin number
plt.figure()
plt.plot(n, fft_mag, label="FFT Magnitude dB")
plt.xlabel("FFT Bin Number")
plt.ylabel("Freq")
plt.grid()
plt.legend()
plt.show()

#-----------------------------------------------------------

freq_baseband = np.fft.fftfreq(fft_bins.size, d=1/Fs)
freq_baseband = np.fft.fftshift(freq_baseband)
freq_rf = freq_baseband + fc

print(f"[INFO] Frequency 511: {freq_rf[511]}")
print(f"[INFO] Frequency 512: {freq_rf[512]}")
print(f"[INFO] Frequency 1023: {freq_rf[1023]}")

print(f"[INFO] freq shape: {freq_rf.shape}")
print(f"[INFO] freq dtype: {freq_rf.dtype}")

# Plotting frequency against bin number
plt.figure()
plt.plot(n, freq_rf, label="Freq")
plt.xlabel("FFT Bin Number")
plt.ylabel("Freq")
plt.grid()
plt.legend()
plt.show()

#-----------------------------------------------------------

#Plotting FFT magnitudes vs frequency
plt.figure()
plt.plot(freq_rf, fft_mag, label="FFT Magnitude dB")
plt.xlabel("RF Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.legend()
plt.show()

print(f"[INFO] Frequency 0: {freq_rf[0]}")
print(f"[INFO] Frequency 512: {freq_rf[512]}")
print(f"[INFO] Frequency 1023: {freq_rf[1023]}")

#-----------------------------------------------------------

