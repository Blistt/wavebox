"""
This script is used to, given a query audio file, identify the most musically similar audio file
in a database of audio files
"""

from utils import random_sample
import numpy as np
from musicnn.musicnn.extractor import extractor
import pathlib
from sklearn.neighbors import NearestNeighbors
import librosa


def get_musical_embedding(filename, model='MTT_musicnn', representation='taggram', temporally_averaged=True):
    # use the musicnn feature extractor to get the embeddings
    taggram, tags, features = extractor(filename, model=model, extract_features=True)

    if representation == 'taggram':
        representation = taggram
    elif representation == 'features':
        representation = features['penultimate']

    if temporally_averaged:
        representation = np.mean(representation, axis=0)

    return representation

def get_embeddings_from_dir(directory, model='MTT_musicnn', representation='taggram', temporally_averaged=True):
    embeddings = []
    songs = []
    for file in pathlib.Path(directory).iterdir():
        songs.append(file)
        # Load the audio file using librosa
        filename = str(file)
        print('getting embedding for', filename)
        embedding = get_musical_embedding(filename, model=model, representation=representation, 
                                          temporally_averaged=temporally_averaged)
        embeddings.append(embedding)
    return embeddings, songs


if __name__ == '__main__':
    # --------------------------------- Input parameters ---------------------------------
    candidates_dir = 'dev_dataset/train/samples'
    model = 'MSD_musicnn'                   # 'MTT_musicnn' or 'MSD_musicnn' or 'MSD_musicnn_big'
    representation = 'features'             # 'taggram' or 'features'
    temporally_averaged = True

    query_files = ['dev_dataset/test/Slipknot - Wait And Bleed (Audio).mp3']
    #--------------------------------------------------------------------------------------

    # Load candidate files and get their embeddings
    candidate_embeddings, songs = get_embeddings_from_dir(candidates_dir, model=model, 
                                                          representation=representation,
                                                          temporally_averaged=temporally_averaged)

    # Fit a nearest neighbors model to candidate embeddings
    candidate_embeddings = np.array(candidate_embeddings)
    candidate_embeddings = candidate_embeddings.reshape(candidate_embeddings.shape[0], -1)
    print(candidate_embeddings.shape)
    E = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(candidate_embeddings)

    # Load the query file and get its embedding
    for query_file in query_files:
        query_sample_filename = f"{'/'.join(query_file.split('/')[:-1])}/samples/{query_file.split('/')[-1]}"
        query_sample = random_sample(query_file, 10)
        librosa.output.write_wav(query_sample_filename, query_sample, 22050)    # save the query sample using librosa
        query_embedding = get_musical_embedding(query_sample_filename, model=model, 
                                                representation=representation, 
                                                temporally_averaged=temporally_averaged)

        # Find the nearest neighbor
        query_embedding = query_embedding.reshape(1, -1)
        distances, indices = E.kneighbors(query_embedding)

        # prints results: recommended song for the given qury song
        query_song = query_file.split('/')[-1].split('.')[0]
        recommended_song = songs[indices[0][0]].name.split('.')[0]
        print('\n', '---------------------------------------------------------------------------------------------')
        print(f"Query song: {query_song}")
        print(f"Recommended song: {recommended_song}", '\n')


