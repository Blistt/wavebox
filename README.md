This project implements a radio station retrieval system. Given a query song, it tunes into the radio station playing the most similar music. 
The system works by doing the following:
1) Tunes into a given number of radio stations and downloads audio samples from each
    - Keny completed a script that tunes to a radio station and downloads an audio sample
    * Need to modularize script to perform the same for a given list of stations
    * Need to format the audio to mp3
    * Need to make sure the audio file is titled "{frequency-of-the-station-in-Mhz}.mp3", e.g., "93_3.mp3"
3) Computes musical similarity between the query song and each of the retrieved audio samples
    - Francisco completed a musical similarity encoder using musicnn pre-trained embeddings
    * Need to experiment with different parameters (model choice, temporally averaged taggram vs non-averaged or feature vectors)
    * Need to obtain team's opinion on parameter choice
5) Tunes into the station corresponding to the sample for which the highest musical similarity was identified
