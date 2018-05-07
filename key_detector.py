import numpy as np
import librosa.feature
import librosa
from loader import Data
from concurrent.futures import ProcessPoolExecutor

# from blue_temp import template
# from template import template
from temp_KS import template


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

    return (result.argmax()+3) % 24

    # major = result[tone]
    # minor = result[tone + 12]
    #
    # if major > minor:
    #     return (result.argmax() + 3) % 12  # convert to gtzan key
    # else:
    #     return (result.argmax() + 3) % 12 + 12  # convert to gtzan key


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
        # f = open("result/Q2_%d.txt" % gamma, 'w')
        aucs = []
        aucs_q1 = []
        print("gamma =", gamma)

        for genre in genres:

            d = Data(genre)
            counter = 0
            counter_q1 = 0

            # Parallelization of  the load file process
            with ProcessPoolExecutor(max_workers=10) as executor:
                for au, sr, key, file_name in executor.map(d.__getitem__, range(d.len)):
                    key_pred = match_key(au, sr, gamma)
                    # print(file_name + "%d" % key_pred , flush=True, file=f)
                    counter += q3_score(key, key_pred)
                    if key == key_pred:
                        counter_q1 += 1

            auc = counter / d.len
            auc_q1 = counter_q1 / d.len
            # print(genre, "auc =", auc, "\n")
            aucs.append(auc)
            aucs_q1.append(auc_q1)


        result_q1 = list(zip(genres, aucs_q1))
        result = list(zip(genres, aucs))
        print(result_q1)
        print(result)


    """
    Q1:
    
    gamma = 100
    [('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]

    
    """



    """
    Q2:
    
    gamma = 1
    [('pop', 0.22), ('blues', 0.06), ('metal', 0.07), ('rock', 0.25), ('hiphop', 0.02)]
    
    gamma = 10
    [('pop', 0.19), ('blues', 0.07), ('metal', 0.06), ('rock', 0.22), ('hiphop', 0.02)]
    
    gamma = 100
    [('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]
    
    gamma = 1000
    [('pop', 0.15), ('blues', 0.07), ('metal', 0.05), ('rock', 0.16), ('hiphop', 0.01)]
    
    """




    """
    Q3:
    gamma = 1
    [('pop', 0.33100000000000007), ('blues', 0.09300000000000001), ('metal', 0.11800000000000005), ('rock', 0.365), ('hiphop', 0.05999999999999999)] 
    
    gamma = 10
    [('pop', 0.31700000000000006), ('blues', 0.12200000000000001), ('metal', 0.11200000000000003), ('rock', 0.3440000000000001), ('hiphop', 0.06)] 
    
    gamma = 100
    [('pop', 0.30500000000000005), ('blues', 0.139), ('metal', 0.10200000000000004), ('rock', 0.30600000000000005), ('hiphop', 0.045)] 

    gamma = 1000
    [('pop', 0.30500000000000005), ('blues', 0.134), ('metal', 0.10500000000000004), ('rock', 0.30400000000000005), ('hiphop', 0.04999999999999999)] 
    """

    """
    Q4
    
    gamma = 1
    [('pop', 0.47), ('blues', 0.27), ('metal', 0.26), ('rock', 0.37), ('hiphop', 0.09)]
    [('pop', 0.5409999999999999), ('blues', 0.28300000000000003), ('metal', 0.311), ('rock', 0.46699999999999997), ('hiphop', 0.14100000000000001)]
    
    gamma = 10
    [('pop', 0.45), ('blues', 0.26), ('metal', 0.22), ('rock', 0.35), ('hiphop', 0.09)]
    [('pop', 0.518), ('blues', 0.28300000000000003), ('metal', 0.278), ('rock', 0.45699999999999996), ('hiphop', 0.131)]
    
    gamma = 100
    [('pop', 0.43), ('blues', 0.21), ('metal', 0.21), ('rock', 0.32), ('hiphop', 0.09)]
    [('pop', 0.493), ('blues', 0.23800000000000002), ('metal', 0.281), ('rock', 0.42700000000000005), ('hiphop', 0.131)]
    
    gamma = 1000
    [('pop', 0.43), ('blues', 0.2), ('metal', 0.21), ('rock', 0.31), ('hiphop', 0.09)]
    [('pop', 0.503), ('blues', 0.228), ('metal', 0.281), ('rock', 0.419), ('hiphop', 0.126)]

    
    """