# This scripts tests pyrtlsdr is working and that it can see the rtl-sdr dongle

from rtlsdr import RtlSdr
import numpy as np

sdr = RtlSdr()

try:
    # Configure the SDR
    sdr.sample_rate = 2.4e6     # 2.4 MS/s
    sdr.center_freq = 100e6     # 100 MHz
    sdr.gain = "auto"
    
    print("[INFO] RTL-SDR opened successfully")
    print(f"[INFO] Sample Rate: {sdr.sample_rate / 1e6:.2f} MS/s")
    print(f"[INFO] Centre frequency: {sdr.center_freq / 1e6:.2f} MHz")
    
    # Capture complex IQ samples
    samples = sdr.read_samples(256 * 1024)
    
    print(f"[INFO] Samples Received: {len(samples)}")
    print(f"[INFO] First IQ Sample: {samples[0]}")
    
    power = np.mean(np.abs(samples) ** 2)
    print(f"[INFO] Average Power: {10 * np.log10(power):.2f} dB")
    
    print("\n[PASS] RTL-SDR test PASSED!")
    
except:
    print("\n[FAIL] RTL-SDR test FAILED!")
    
finally:
    sdr.close()