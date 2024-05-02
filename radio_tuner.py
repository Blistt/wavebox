'''
This script is used to tune the radio to a specific frequency and listen to that station indefinitely.
The script should allow a user to:
- specify the frequency
'''
import numpy as np
from rtlsdr import RtlSdr
from scipy import signal
import sounddevice as sd

def stream_radio(Freq, sampling_rate=1140000):
    print(f'Streaming radio at {Freq} MHz.')

    sdr = RtlSdr()

    # Configure SDR
    Freq = Freq * 1e6  # Convert frequency to Hz
    F_offset = 250000  # Offset to avoid DC spike in SDR
    Fc = Freq - F_offset  # Actual center frequency to tune

    sdr.sample_rate = sampling_rate  # Set sampling rate
    sdr.center_freq = Fc  # Set center frequency
    sdr.gain = 'auto'  # Enable automatic gain control

    try:
        while True:
            # Read a block of samples from the SDR
            samples = sdr.read_samples(256*1024)
            # Convert the raw complex samples to a NumPy array for processing
            x1 = np.array(samples).astype("complex64")
            # Apply frequency correction to shift the samples down by the offset
            fc1 = np.exp(-1.0j * 2.0 * np.pi * F_offset / sampling_rate * np.arange(len(x1)))
            x2 = x1 * fc1

            # Define and apply a low-pass filter to isolate the FM signal
            bandwidth = 200000  # Bandwidth for FM signals
            n_taps = 64  # Number of taps in the filter
            lpf = signal.remez(n_taps, [0, bandwidth, bandwidth + (sampling_rate / 2 - bandwidth) / 4, sampling_rate / 2], [1, 0], Hz=sampling_rate)
            x3 = signal.lfilter(lpf, 1.0, x2)

            # Decimate the signal to reduce the sampling rate appropriate for audio
            dec_rate = int(sampling_rate / bandwidth)
            x4 = x3[0::dec_rate]
            Fs_y = sampling_rate / dec_rate

            # Demodulate the FM signal by calculating the phase difference between consecutive samples
            y5 = x4[1:] * np.conj(x4[:-1])
            x5 = np.angle(y5)

            # Apply a de-emphasis filter to the demodulated signal to improve audio quality
            d = Fs_y * 50e-6  # De-emphasis time constant for FM in US
            x = np.exp(-1/d)
            x6 = signal.lfilter([1-x], [1, -x], x5)

            # Further reduce the sampling rate to match standard audio playback rates
            audio_freq = 48000
            dec_audio = int(Fs_y / audio_freq)
            x7 = signal.decimate(x6, dec_audio)
            x7 *= 32767 / np.max(np.abs(x7))  # Normalize audio to int16 range

            # Play the processed audio
            sd.play(x7.astype("int16"), samplerate=audio_freq)
            sd.wait()

    except KeyboardInterrupt:
        print("Radio stream stopped.")
        sdr.close()

if __name__ == "__main__":
    stream_radio(94.7)  # Example frequency
