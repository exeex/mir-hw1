import numpy as np
import librosa.feature
import librosa
from loader import Data
import scipy.io.wavfile as wav
import scipy.signal

from template import template


def R(x: np.ndarray, y: np.ndarray):
    a = sum([(x[k] - x.mean()) * (y[k] - y.mean()) for k in range(12)])
    b = sum([(x[k] - x.mean()) ** 2 * (y[k] - y.mean()) ** 2 for k in range(12)]) ** 0.5
    return a / b


def match_Key(au, sr, gamma):
    chroma = np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y=au, sr=sr)))

    chroma = chroma / np.tile(np.sum(np.abs(chroma) ** 2, axis=0) ** (1. / 2),
                              (chroma.shape[0], 1))  # normalize chroma

    vector = np.sum(chroma, axis=1)
    result = np.array([R(template[k], vector) for k in range(24)])

    return (result.argmax() + 3) % 24  # convert to gtzan key


genres = ['pop', 'blues', 'metal', 'rock', 'hiphop']
aucs = []

for genre in genres:

    d = Data(genre)
    counter = 0

    for data in d:

        au, sr, key = data
        key_pred = match_Key(au, sr, gamma=100)

        print(key_pred,key)

        if key == key_pred:
            counter+=1

    auc = counter / d.len
    print("auc", auc)
    aucs.append(auc)

result = list(zip(genres,aucs))
print(result)


"""
result:
[('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]
"""