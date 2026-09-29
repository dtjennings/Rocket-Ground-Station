This document includes my notes around IQ samples.

----

What are I and Q samples and why do we use them?

If we consider the complex sinusoid x[n]=Ae^((j2πf_0 n)/f_s ) , if we were to use Euler’s identity,

e^jθ=cosθ+jsinθ

We get: 
e^jθ=Acos((2πf_0 n)/f_s )+Ajsin((2πf_0 n)/f_s )

Therefore:
I[n]= Acos((2πf_0 n)/f_s )
Q[n]= Ajsin((2πf_0 n)/f_s )

Plotting Q against I, that complex sinusoid moved around a circle centred on the origin.

----

I[n] and Q[n] are two parts of the same signal. At each sample n, they are the horizontal and vertical coordinates of one complex sample.

I am going to create a program which visualises these samples, so to demonstrate that complex sinusoids move around a circle centred on the orignin.

This will show three plots:
1. I[n] vs sample number
2. Q[n] vs sample number
3. Q[n] vs I[n]
