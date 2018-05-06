import numpy as np
import librosa.feature
import librosa
from loader import Data
from concurrent.futures import ProcessPoolExecutor

# from blue_temp import template
from template import template


def R(x: np.ndarray, y: np.ndarray):
    """
    :param x: template or chroma vector
    :param y: template or chroma vector
    :return: correlation coefficient between x, y
    """

    a = sum([(x[k] - x.mean()) * (y[k] - y.mean()) for k in range(12)])
    b1 = sum([(x[k] - x.mean()) ** 2 for k in range(12)]) ** 0.5
    b2 = sum([(y[k] - y.mean()) ** 2 for k in range(12)]) ** 0.5

    return a / (b1 * b2)


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

    tone = vector.argmax()

    result = np.array([R(template[k], vector) for k in range(24)])

    major = result[tone]
    minor = result[tone + 12]

    if major > minor:
        return (result.argmax() + 3) % 12  # convert to gtzan key
    else:
        return (result.argmax() + 3) % 12 + 12  # convert to gtzan key


def q3_score(ans, preds):
    new_accuracy = 0

    pr = preds
    la = ans
    if pr == la:
        new_accuracy += 1.
    if pr < 12 and la < 12:
        if pr == (la + 7) % 12:
            new_accuracy += 0.5
    elif pr >= 12 and la >= 12:
        pr -= 12
        la -= 12
        if pr == (la + 7) % 12:
            new_accuracy += 0.5

    # Relative major/minor
    if pr < 12 <= la:
        la -= 12
        if pr == (la + 3) % 12:
            new_accuracy += 0.3
    elif pr >= 12 and la < 12:
        pr -= 12
        if ((pr + 3) % 12 == la):
            new_accuracy += 0.3

    # Parallel major/minor
    if pr == (la + 12) % 24:
        new_accuracy += 0.2

    return new_accuracy


if __name__ == "__main__":

    genres = ['pop', 'blues', 'metal', 'rock', 'hiphop']

    for gamma in [1, 10, 100, 1000]:
        aucs = []
        print("gamma =", gamma)

        for genre in genres:

            d = Data(genre)
            counter = 0

            # Parallelization of the load file process
            with ProcessPoolExecutor(max_workers=4) as executor:
                for au, sr, key in executor.map(d.__getitem__, range(d.len)):
                    key_pred = match_key(au, sr, gamma)
                    # print("[%d,%d]" % (key, key_pred), end=' ', flush=True)
                    counter = counter + q3_score(key, key_pred)
                    # if key == key_pred:
                    #     counter += 1

            auc = counter / d.len
            print(genre, "auc =", auc, "\n")
            aucs.append(auc)

        result = list(zip(genres, aucs))
        print("----------------------------------------------\n",result,"\n------------------------------------------\n")

"""
result:

[('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]

"""
