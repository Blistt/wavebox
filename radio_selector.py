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


def get_musical_embedding(filename, model='MTT_musicnn'):
    # use the musicnn feature extractor to get the embeddings
    taggram, tags, features = extractor(filename, model=model, extract_features=True)
    average_taggram = np.mean(taggram, axis=0)
    return average_taggram

def get_embeddings_from_dir(directory, model='MTT_musicnn'):
    embeddings = []
    songs = []
    for file in pathlib.Path(directory).iterdir():
        songs.append(file)
        # Load the audio file using librosa
        filename = str(file)
        print('getting embedding for', filename)
        embedding = get_musical_embedding(filename, model=model)
        embeddings.append(embedding)
    return embeddings, songs


if __name__ == '__main__':
    # Load candidate files and get their embeddings
    candidates_dir = 'dev_dataset/train/samples'
    candidate_embeddings, songs = get_embeddings_from_dir(candidates_dir)

    # Fit a nearest neighbors model to candidate embeddings
    candidate_embeddings = np.array(candidate_embeddings)
    candidate_embeddings = candidate_embeddings.reshape(candidate_embeddings.shape[0], -1)
    print(candidate_embeddings.shape)
    E = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(candidate_embeddings)

    # Load the query file and get its embedding
    query_file = 'dev_dataset/test/summer_vivaldi.mp3'
    query_sample_filename = f"{'/'.join(query_file.split('/')[:-1])}/samples/{query_file.split('/')[-1]}"
    query_sample = random_sample(query_file, 10)
    librosa.output.write_wav(query_sample_filename, query_sample, 22050)    # save the query sample using librosa
    query_embedding = get_musical_embedding(query_sample_filename)

    # Find the nearest neighbor
    query_embedding = query_embedding.reshape(1, -1)
    distances, indices = E.kneighbors(query_embedding)

    # prints results: recommended song for the given qury song
    query_song = query_file.split('/')[-1].split('.')[0]
    recommended_song = songs[indices[0][0]].name.split('.')[0]
    print('\n', '---------------------------------------------------------------------------------------------')
    print(f"Query song: {query_song}")
    print(f"Recommended song: {recommended_song}", '\n')


