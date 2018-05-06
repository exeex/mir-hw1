import numpy as np
import librosa.feature
import librosa
from loader import Data
from concurrent.futures import ProcessPoolExecutor

from template import template


def R(x: np.ndarray, y: np.ndarray):
    """
    :param x: template or chroma vector
    :param y: template or chroma vector
    :return: correlation coefficient between x, y
    """

    a = sum([(x[k] - x.mean()) * (y[k] - y.mean()) for k in range(12)])
    b = sum([(x[k] - x.mean()) ** 2 * (y[k] - y.mean()) ** 2 for k in range(12)]) ** 0.5
    return a / b


def match_key(au, sr, gamma):
    """
    :param au: audio file
    :param sr: sample rate
    :param gamma: gamma parameter of nonlinear transform
    :return: key label
    """

    chroma = np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y=au, sr=sr)))

    chroma = chroma / np.tile(np.sum(np.abs(chroma) ** 2, axis=0) ** (1. / 2),
                              (chroma.shape[0], 1))  # normalize chroma

    vector = np.sum(chroma, axis=1)
    result = np.array([R(template[k], vector) for k in range(24)])

    return (result.argmax() + 3) % 24  # convert to gtzan key


if __name__ == "__main__":

    genres = ['pop', 'blues', 'metal', 'rock', 'hiphop']
    aucs = []

    for genre in genres:

        d = Data(genre)
        counter = 0

        # Parallelization of the load file process
        with ProcessPoolExecutor(max_workers=10) as executor:
            for au, sr, key in executor.map(d.__getitem__, range(d.len)):

                key_pred = match_key(au, sr, gamma=100)
                print(key_pred, key)

                if key == key_pred:
                    counter += 1

        auc = counter / d.len
        print("auc", auc)
        aucs.append(auc)

    result = list(zip(genres, aucs))
    print(result)

    """
    result:
    
    [('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]
    
    """
