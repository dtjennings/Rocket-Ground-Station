This document contains my notes around DC offset.

----
What DC offset actually is in an SDR IQ?

First to understand DC offset. Suppose an ADC gives you a sequence: x[n]
Where n is the sample number. If we measured: x[n]=1,2,1,0,-1,-2,-1,0,…
The waveform oscillates around zero. Its average is:

1/N ∑_(n=0)^(N-1)[x[n]   ≈  0]

Now imagine every sample has accidently had +3 added: x_m=x[n]+3
The waveform still contains the original oscillation, but it now oscillates around 3 instead of zero. It’s mean becomes approximately 3.
That constant 3 is a DC offset.

----

Why call it DC?

A constant doesn’t change with time. A CT DC signal would simply be x(t)=A and it’s frequency is f=0 Hz. The sampled equivalent is x[n]=A for every n. So, in DSP, DC means the zero-frequency component of the signal.

An SDR gives two signals: I and Q. We combine them into one complex signal:
 x[n]=I[n]+jQ[n]

 ----

Our receiver might produce:
I_measured[n] = I_signal[n] + I_DC
Q_measured[n] = Q_signal[n] + Q_DC

Therefore the sample is:
x[n] = I_signal[n] + I_DC + j(Q_signal[n] + Q_DC)

x[n] = I_signal[n] + jQ_signal[n] + I_DC + jQ_DC

x[n] = x_signal[n] + DC_offset

----

Why do SDR receivers produce a DC offset?

The receiver mixes an RF signal down toward baseband. Ideally, RF energy exactly at the tuned centre frequency becomes: f_baseband = 0.

That makes DC imperfections awkward because the receiver's own zero-frequency artefacts appear in the same part of the spectrum.

Several effects can contribute:
- ADC or analogue offsets
- LO leakage and mixer self-mixing
- Digital offsets

----

Why does DC offset matter?

A DC spur means part of the receiver's apparent signal power isn't coming from the rocket transmitter at all. That can affect later algorithms. For signal power estimation, a dc offset adds additional power, causing you to overestimate received signal power.
For weak signal detection, a large centre spur can reduce visibility of useful components close to the tunes centre.

For LoRa, a constant IQ offset doesn't corrupt every LoRa symbol. But a sufficiently strong centre-frequency component can interfere with detection metrics, spectral analysis, and some implementations of preamble/symbol processing.

----

Need to be careful when estimating doppler. Doppler information can correspond to small frequency shifts around a reference frequency. A DC removal algorithm is designed to suppress very low frequency content. So an aggressive DC remover could potentially suppress information I need near zero doppler.

This is a reason not to immediately subtract a running average.

----

I_DC ~= mean(I)
Q_DC ~= mean(Q)

This only estimates the unwanted DC correctly when the wanted signal itself has sufficiently small mean over the observation interval.

----

The method of calculating and subtracting the average always forces the output block mean to zero.
This matters for Doppler/ranging, because a legitimate wanted component close to DC could be attenuated or removed.

This estimator makes the assumption that everything at DC is unwanted.

x_m[n] = x[n] + d where d is the unwanted dc offset

estimate it by calculating the mean of x_m. Then subtract,
y[n] = x_m[n] - mean(d)



----

