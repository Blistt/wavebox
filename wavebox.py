'''
Master wavebox module: asks the user for an audio file, then samples the radio stations in the local area, calculates
musical similarity between the user provided audio file and the sampled radio stations, identifies the radio station frequency
playing the most similar music and tunes into this radio station
'''

import radio_sampler
import radio_selector

def wavebox(input_audio):

    radio_stations = [88.5,
                      89.5,
                      92.3,
                      93.1,
                      93.5,
                      93.9,
                      94.7,
                      95.5,
                      96.3,
                      97.5,
                      98.3,
                      99.5,
                      99.9,
                      100.7,
                      102.1,
                      103.5,
                      104.3,
                      105.1,
                      105.9,
                      106.7]
    
    for station in radio_stations:
        radio_sampler.sample_signal(station)
    

if __name__ == "__main__":
    audio_file_path = "path/to/audioInput.mp3"
    wavebox(audio_file_path)
