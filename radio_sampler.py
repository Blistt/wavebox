#  Capture the FM radio signals, demodulate them, play the audio in wav file saved in same directory, 
#  and also plots the first 10,000 samples of the captured signal.


import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
from scipy import signal
import numpy as np
import os
import time
from scipy.io import wavfile
from pydub import AudioSegment
import sounddevice


def sample_signal(Freq):

    # Create an RtlSdr object
    sdr = RtlSdr()

    # Configure Device
    #Freq = 91.7  # Frequency in MHz
    Freq = Freq * 1e6 # Convert to Hz
    # Freqs = []  # List of frequencies in radio_Selector.py
    Fs = 1140000  # Sampling Rate
    F_offset = 250000  # Frequency Offset
    Fc = Freq - F_offset  # Center Frequency

    # Configure the rtlsdr device with the specified sampling rate, 
    # center frequency, and gain mode.
    sdr.sample_rate = Fs
    sdr.center_freq = Fc
    sdr.gain = 'auto'

    start_time = time.time() # Start time of capturing signal
    # Max number of samples read from RTL-SDR device
    samples = sdr.read_samples(8192000)
    end_time = time.time() # End time of capturing signal
    duration = end_time - start_time

    print(f"The sampling process took {duration} seconds.")

    # Convert samples into NumPy array
    x1 = np.array(samples).astype("complex64")
    # Frequency correction factor of captured signal
    fc1 = np.exp(-1.0j*2.0*np.pi* F_offset/Fs*np.arange(len(x1)))
    # Multiply each captured sample by the frequency correction factor (fc1)
    x2 = x1 * fc1

    # Display plot of first 10,000 samples of the captured signal
    # The more samples we plot (i.e 20,000), the more congested the plot appears
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

    # Calculating the phase difference between x4 samples 
    y5 = x4[1:] * np.conj(x4[:-1])
    x5 = np.angle(y5)

    # 75e-6 is standard for FM broadcasting in UK, 50e-6 is standard for US
    d = Fs_y * 50e-6 # Calculate time constant
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

    # Load wav file into AudioSegment object
    wav_audio = AudioSegment.from_wav("wav.wav")
    #raw_audio = AudioSegment.from_file("audio.wav", format="raw", frame_rate=44100, channels=2, sample_width=2)

    # Export the audio to MP3 format
    wav_audio.export(f"{Freq}.mp3", format="mp3")
    #raw_audio.export("audio2.mp3", format="mp3")

    # Removes the WAV file after exporting it to MP3 format
    os.remove('C:\\Users\\offda\\OneDrive\\Desktop\\radiovenv\\envs\\wav.wav')

# Because this file will be called by another, a main isn't needed. Will be removed soon
if __name__ == "__main__":
    sample_signal(91.7)
    print("Audio playback complete.")

    # This needs to be in radio_selector.py.
    #import radio_sampler
    # 
    # Pass the frequency of the radio station to be sampled as an argument.
    #radio_sampler.sample_signal(x.y) # x.y is the frequency of the radio station to be sampled (i.g. 91.7).
    #
    # This will need to be in the audio input file (user interface). I will name the file audio_input.py
    #import radio_selector
    #
    # radio_selector will need a method to be called and to pass the .mp3 to.
    #audio_file_path = "path/to/audioInput.mp3"
    #radio_selector.<methodName>(audio_file_path)