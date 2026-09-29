##############################################################################
# This program investigates the effects of DC offset experimentally
##############################################################################

#-------------------------------------------------------------
# Libraries
#-------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

#-------------------------------------------------------------
# Signal Parameters
#-------------------------------------------------------------

f_s = 1_000_000
f_0 = 103_271
N = 4096

A = 0.5
I_dc = 0.2
Q_dc = -0.1

#-------------------------------------------------------------
# Generate Signals
#-------------------------------------------------------------

n = np.arange(N)

x_clean = A * np.exp(1j * 2 * np.pi * f_0 * n / f_s)
x_dc = x_clean + I_dc + 1j*Q_dc

I_clean = np.real(x_clean)
Q_clean = np.imag(x_clean)

I_dc_sig = np.real(x_dc)
Q_dc_sig = np.imag(x_dc)

#-------------------------------------------------------------
# Time Domain Representation of I
#-------------------------------------------------------------

plt.figure()

plt.plot(n[:50], I_clean[:50], label="Clean I")
plt.plot(n[:50], I_dc_sig[:50], label="I with DC")

plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.show()

#-------------------------------------------------------------
# Time Domain Representation of Q
#-------------------------------------------------------------

plt.figure()

plt.plot(n[:50], Q_clean[:50], label="Clean Q")
plt.plot(n[:50], Q_dc_sig[:50], label="Q with DC")

plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.show()

#-------------------------------------------------------------
# IQ Plane
#-------------------------------------------------------------

plt.figure()

plt.scatter(I_clean[:100], Q_clean[:100], s=10, label="Clean")
plt.scatter(I_dc_sig[:100], Q_dc_sig[:100], s=10, label="With DC")

plt.xlabel("I")
plt.ylabel("Q")
plt.axis("equal")
plt.grid()
plt.legend()

plt.show()

#-------------------------------------------------------------
# Frequency Domain Representation of x
#-------------------------------------------------------------

X_clean = np.fft.fftshift(np.fft.fft(x_clean))
X_dc = np.fft.fftshift(np.fft.fft(x_dc))

freq = np.fft.fftshift(np.fft.fftfreq(N, d=1/f_s))

mag_clean = 20 * np.log10(np.abs(X_clean) + 1e-12)
mag_dc = 20 * np.log10(np.abs(X_dc) + 1e-12)

plt.figure()

plt.plot(freq, mag_clean, label="Clean")
plt.plot(freq, mag_dc, label="With DC")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.legend()

plt.show()

#-------------------------------------------------------------
# Measuring the Mean
#-------------------------------------------------------------

print(f"Mean clean I: {round(np.mean(I_clean), 2)}")
print(f"Mean clean Q: {round(np.mean(Q_clean), 2)}")

print(f"Mean corrupted I: {round(np.mean(I_dc_sig), 2)}")
print(f"Mean corrupted Q: {round(np.mean(Q_dc_sig), 2)}")

print(f"Complex mean, clean: {np.mean(x_clean)}")
print(f"Complex mean, with DC: {np.mean(x_dc)}")

