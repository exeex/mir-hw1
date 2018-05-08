import numpy as np
import librosa.feature
import librosa
from concurrent.futures import ProcessPoolExecutor
from local_loader import d, key_map
from sklearn import svm

from sklearn.multiclass import OneVsOneClassifier

counter = 0




m = OneVsOneClassifier(svm.SVC(decision_function_shape='ovo', kernel='rbf'))



# train
with ProcessPoolExecutor() as executor:
    X = np.empty((0, 12 * d.window))
    keys = []

    for song, key, file, txt in executor.map(d.__getitem__, range(1, 10)):

        X2 = np.empty((0, 12 * d.window))

        for idx, item in enumerate(song):
            X2 = np.concatenate((X2, item.reshape((1, 120))), axis=0)
        keys.extend(key)

        if X2.shape[0] > len(key):
            X2 = X2[:len(key), :]
        else:
            key = key[:X2.shape[0]]

        print(X2.shape, len(key), file, txt, flush=True)

        X = np.concatenate((X, X2), axis=0)

    if X.shape[0] > len(keys):
        X2 = X[:len(keys), :]
    else:
        keys = keys[:X.shape[0]]

    m.fit(X, np.array(keys))

counter = 0
total = 0

# test
with ProcessPoolExecutor(max_workers=10) as executor:

    X = np.empty((0, 12 * d.window))
    keys = []

    for song, keys, file, txt in executor.map(d.__getitem__, range(10, 15)):
        for idx, item in enumerate(song):
            if idx == len(keys): break
            key_pred = m.predict(item.reshape((1, 120)))
            print(keys[idx], key_pred[0])
            if keys[idx] == key_pred[0]:
                counter += 1
            total += 1

print("auc=", counter / total)


"""
auc= 0.3909002904162633

"""