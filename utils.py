import librosa
import numpy as np
import os
import pathlib

def random_sample(filename, duration, save=False):
    # Load the audio file
    y, sr = librosa.load(filename)

    # Compute the total length of the audio in seconds
    total_duration = librosa.get_duration(y=y, sr=sr)

    # Make sure the requested duration is not longer than the total duration of the audio
    if duration > total_duration:
        print("The requested duration is longer than the total duration of the audio.")
        return None

    # Compute the starting point of the sample
    start = np.random.uniform(0, total_duration - duration)

    # Convert the start time and duration to samples
    start_sample = librosa.time_to_samples(start, sr=sr)
    duration_samples = librosa.time_to_samples(duration, sr=sr)

    # Extract the sample
    sample = y[start_sample : start_sample + duration_samples]

    if save:
        song = filename.split("/")[-1]
        # save the sample as an mp3 file
        librosa.output.write_wav(f'dev_dataset/samples/{song}', sample, sr=22050)

    return sample


def sample_from_dir(directory, duration):
    directory = pathlib.Path(directory)

    # Get samples for all mp3 files in a directory
    for file in directory.glob('*.mp3'):
        print(file)
        sample = random_sample(file, duration)

        # Saves the samples as mp3 files
        output_dir = directory / 'samples'
        output_dir.mkdir(exist_ok=True)
        output_filename = output_dir / file.name
        print('saving', output_filename)
        librosa.output.write_wav(str(output_filename), sample, sr=22050)
    
    

if __name__ == '__main__':
    directory = 'dev_dataset/train'

    sample_from_dir(directory, 10)
