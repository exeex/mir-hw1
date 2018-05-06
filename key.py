import numpy as np
import librosa.feature
import librosa
from loader import Data
import scipy.io.wavfile as wav
import scipy.signal



# Generate major chord templates
Major_template = np.array([[1,0,0,0,1,0,0,1,0,0,0,0]])/np.sqrt(3.0)
# Generate monor chord templates
Minor_template = np.array([[1,0,0,1,0,0,0,1,0,0,0,0]])/np.sqrt(3.0)
Template = Major_template


for i in range(11):
    Template = np.append(Template, np.roll(Major_template, i+1), axis=0)
for i in range(12):
    Template = np.append(Template, np.roll(Minor_template, i), axis=0)

def Match_Key(au, sr, gamma):

    Chroma = np.log(1 + gamma * np.abs(librosa.feature.chroma_cens(y = au, sr = sr)))
    Chroma = Chroma / np.tile(np.sum(np.abs(Chroma) ** 2, axis = 0) ** (1. / 2),
                            (Chroma.shape[0], 1)) # normalize chroma
    Result = np.dot(Template, np.sum(Chroma, axis=1))
    Chord = (Result.argmax() + 3) % 24  # convert to gtzan key
    return Chord


d = Data()

au, sr, key = d[0,1]

key_pred = Match_Key(au, sr, gamma=100)





