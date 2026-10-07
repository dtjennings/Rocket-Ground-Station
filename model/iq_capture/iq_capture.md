Max Sample Rate = 2.4 MHz

- rtl-sdr apparently has sensitivity of -133 dBm.
- 8 bit samples - 2 bytes per IQ sample

- Kracken SDR for direction of arrival. £1800

https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/

-----------------------------------------------------

RTL-SDR IQ
    |
DC Offset removal
    |
Channel Selection/ Low-Pass Filtering
    |
Frequency Correction
    |
Resampling
    |
LoRa Packet Detection
    |
Preamble Detection
    |
Symbol Timing Synchronisation
    |
Generate Reference Downchirp
    |
Multiply Received symbol by reference downchirp
    |
FFT
    |
find FFT peak
    |
Convert FFT-bin position into LoRa symbol
    |
Repeat for packet symbols
    |
Deinterleave / dewhiten / FEC
    |
Recover payload

-----------------------------------------------------

pip install "pyrtlsdr[lib]" numpy

To check python sees the dongle:
python -c "from rtlsdr import RtlSdr; devices = RtlSdr.get_device_serial_addresses(); print('RTL-SDR devices:', devices); print('Count:', len(devices))"


Should see:
RTL-SDR devices: ['00000001']                                                                                           Count: 1  


------------------------------------------------------

The rtlsdr library will still need to be used on the KR260. It will be used on the PS to acquire complex IQ samples. The numpy DSP would instead be done on the FPGA and so numpy wouldn't be used, however, the functions would be similar. Matplotlib could potentially be used to display data on the laptop UI.

-------------------------------------------------------

run test_sdr.py to ensure rtl sdr is being detected.

-------------------------------------------------------

PyRTLSDR documentation

https://pyrtlsdr.readthedocs.io/en/latest/Overview.html#usage

https://github.com/pyrtlsdr/pyrtlsdr/blob/master/rtlsdr/rtlsdr.py

-------------------------------------------------------

Sample rate determines how many complex IQ samples I receive per second.
Fs = 2.4 MS/s

Each IQ sample consists of: I[n] + jQ[n]    -  2 bytes

For complex sampling, the observable spectrum is approximately:
-Fs/2 -> +Fs/2
relative to centre frequency.

The LoRa transmit bandwidth can be configured for 125 kHz or 250 kHz.

-------------------------------------------------------

Centre Frequency controls the tuner. 

the complex baseband samples represent RF frequencies around fc.

The RTL-SDR does not give Python samples oscillating at a frequency. The tuner translates the RF region around the frequency doen to complex baseband.

An FFT may contain offset frequencies from the tuning frequency. I may need to convert them back into RF frequencies using:
RF Frequency = centre frequency + baseband frequency

Rocket flight computer will be transmitting at 869.4-869.65 MHz

-------------------------------------------------------

The gain controls amplification in the RTL-SDR receiver chain.

If gain is too low, the LoRa signal may sit close to the noise floor.
Could there be a problem with too much gain? Is it just a power issue?

We can either set the gain automatically or manually. Manually will probably be better for consistency.

To set the gain to auto:
sdr.gain = "auto"

To observe available gain options:
gains = sdr.get_gains()
print(f"[INFO] Gain: {gains}")

[INFO] Gain: [0, 9, 14, 27, 37, 77, 87, 125, 144, 157, 166, 197, 207, 229, 254, 280, 297, 328, 338, 364, 372, 386, 402, 421, 434, 439, 445, 480, 496]

There may be an issue in the rtl sdr drivers. When I manually configure the gain, then read the gain back, it always returns 0. 
This problem isn't new: https://gnuradio-cookbook.blogspot.com/2024/08/running-rtl-based-sdr-from-python.html

I created ascript gain_test.py to check adjusting the gain has an affect on the signal. I collected samples while configured to the min gain and samples while configures to the max gain, calculated the average power of each then compared.

There was an increase in average power, but not as much as I would have expected.

-------------------------------------------------------

To read samples:
samples = sdr.read_samples(1024)
