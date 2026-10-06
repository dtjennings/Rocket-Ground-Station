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