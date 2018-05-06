import numpy as np
import librosa.feature
import librosa
from loader import Data
import scipy.io.wavfile as wav
import scipy.signal

from template import template



def Match_Key(au, sr, gamma):

    Chroma = np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y = au, sr = sr)))
    Chroma = Chroma / np.tile(np.sum(np.abs(Chroma) ** 2, axis = 0) ** (1. / 2),
                            (Chroma.shape[0], 1)) # normalize chroma


    Result = np.dot(template, np.sum(Chroma, axis=1))


    Chord = (Result.argmax() + 3) % 24  # convert to gtzan key
    return Chord


genres =['pop', 'blues', 'metal', 'rock', 'hiphop']



d = Data(genres[0])


for data in d:

    counter = 0

    au, sr, key = data
    key_pred = Match_Key(au, sr, gamma=100)

    if key == key_pred:
        counter+=1
        print('!')






