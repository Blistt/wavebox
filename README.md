This project implements a radio station retrieval system. Given a query song, it tunes into the radio station playing the most similar music. 
The system works by doing the following:
1) Tunes into a given number of radio stations and downloads audio samples from each
2) Computes musical similarity between the query song and each of the retrieved audio samples
3) Tunes into the station corresponding to the sample for which the highest musical similarity was identified
