##############################################################################
# This program provides a visual representation of IQ samples
##############################################################################

#-------------------------------------------------------------
# Libraries
#-------------------------------------------------------------

import math
import matplotlib.pyplot as plt

#-------------------------------------------------------------
# Signal Parameters
#-------------------------------------------------------------

A = 1       # Amplitude
f_0 = 1     # Sinusoid frequency
f_s = 32    # Sampling frequency

N = f_s / f_0    # Number of samples per cycle

#-------------------------------------------------------------
# Generate Sample Numbers
#-------------------------------------------------------------

sample_index = []

i = 0   # Sample Index
while (i < N):
    sample_index.append(i)
    i+=1 
    
#-------------------------------------------------------------
# Calculate phase for every sample
#-------------------------------------------------------------

sample_phase = []

for n in sample_index:
    w_0 = 2 * math.pi * (f_0 / f_s)     # Phase advance per sample
    phase = w_0 * n
    sample_phase.append(phase)
        
#-------------------------------------------------------------
# Calculate I from cosine
#-------------------------------------------------------------

I = []

for phase in sample_phase:
    I.append(A * math.cos(phase))
    

#-------------------------------------------------------------
# Calculate Q from sine
#-------------------------------------------------------------

Q = []

for phase in sample_phase:
    Q.append(A * math.sin(phase))
    
#-------------------------------------------------------------
# Checking for a constant R
#-------------------------------------------------------------

R = []

for n in sample_index:
    R.append(math.sqrt(I[n]**2 + Q[n]**2))
    
print(R)

#-------------------------------------------------------------
# Plot I against sample number
#-------------------------------------------------------------

plt.subplot(2, 2, 1)
plt.plot(sample_index, I, 'o')

plt.title("I vs Sample")
plt.xlabel("Sample")
plt.ylabel("I")

#-------------------------------------------------------------
# Plot Q against sample number
#-------------------------------------------------------------

plt.subplot(2, 2, 2)
plt.plot(sample_index, Q, 'o')

plt.title("Q vs Sample")
plt.xlabel("Sample")
plt.ylabel("Q")

#-------------------------------------------------------------
# Plot Q against I
#-------------------------------------------------------------

plt.subplot(2, 2, 3)
plt.plot(I, Q, 'o')

plt.title("Q vs I")
plt.xlabel("I")
plt.ylabel("Q")

plt.show()