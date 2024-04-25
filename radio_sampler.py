#  Capture the FM radio signals, demodulate them, play the audio in wav file saved in same directory, 
#  and also plots the first 10,000 samples of the captured signal.


import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
from scipy import signal
import numpy as np
from scipy.io import wavfile
import sounddevice

sdr = RtlSdr()

# Configure Device
Freq = 91.7e6  # frequency in Hz (e.g., 91.7 MHz)
Fs = 1140000  # sampling rate
F_offset = 250000  # frequency offset
Fc = Freq - F_offset  # center frequency

# Configure the rtlsdr device with the specified sampling rate, 
# center frequency, and gain mode.
sdr.sample_rate = Fs
sdr.center_freq = Fc
sdr.gain = 'auto'

# Max number of samples
samples = sdr.read_samples(5700000)

# Convert samples into NumPy array
x1 = np.array(samples).astype("complex64")
# Frequency correction of captured signal
fc1 = np.exp(-1.0j*2.0*np.pi* F_offset/Fs*np.arange(len(x1)))
# Multiply each captured sample by the frequency correction factor (fc1)
x2 = x1 * fc1

# Display plot of first 10,000 samples of the captured signal
plt.figure(figsize=(10, 4))
plt.plot(np.abs(x2[:10000]))
plt.title('Captured Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()

bandwidth = 200000  # Bandwidth of the FM signal 200kHz
n_taps = 64  # Number of filter taps

# Low-Pass Filter using Remez algorithm to filter frequencies beyond bandwidth
lpf = signal.remez(n_taps, [0, bandwidth, bandwidth+(Fs/2-bandwidth)/4, Fs/2], [1,0], Hz=Fs)

# Apply LPF to frequency corrected signal (x2)
x3 = signal.lfilter(lpf, 1.0, x2) 
# Calculate decimation rate
dec_rate = int(Fs / bandwidth)

x4 = x3[0::dec_rate] # Downsample x3 by a factor of dec_rate using slicing
Fs_y = Fs/dec_rate # Sampling rate reduced

# Calculating the ohase difference between x4 samples 
y5 = x4[1:] * np.conj(x4[:-1])
x5 = np.angle(y5)

d = Fs_y * 75e-6 # Calculate time constant
x = np.exp(-1/d)
b = [1-x]
a = [1,-x]
x6 = signal.lfilter(b,a,x5)

# Downsample signal from LPF for audio playback
audio_freq = 48100.0
dec_audio = int(Fs_y/audio_freq)
Fs_audio = Fs_y / dec_audio
x7 = signal.decimate(x6, dec_audio)

# Play audio signal using sounddevice module
sounddevice.play(x7,Fs_audio)
x7 *= 10000 / np.max(np.abs(x7))

# Write audio to a WAV file to hear playback
wavfile.write('wav.wav',int(Fs_audio), x7.astype("int16"))
