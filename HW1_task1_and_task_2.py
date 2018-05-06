import numpy as np
import scipy.linalg
import scipy.stats
import librosa
import numpy as np
import scipy.linalg
import scipy.stats
import glob
from sklearn.metrics import accuracy_score
import pickle
import torch
from torch.autograd import Variable
from scipy.stats import wasserstein_distance, entropy, spearmanr, kendalltau
from scipy.spatial.distance import hamming
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel, laplacian_kernel, polynomial_kernel, \
    manhattan_distances, chi2_kernel, additive_chi2_kernel, cosine_similarity



gammas = [1, 10, 100, 1000]
genres = ['All_genres', 'pop', 'blues', 'metal', 'hiphop', 'rock']
key_types = ["binary", "K-S"]
CLP_methods = [0, 1, 2]
metrics = ["Pearson_correlation_coefficient", "euclidean_distances", "rbf_kernel", "laplacian_kernel", "cosine_similarity"]


# key_type: ks or binary
def finding_key(summed_chroma, key_type, metric="Pearson_correlation_coefficient"):
    summed_chroma = scipy.stats.zscore(summed_chroma)
    if key_type == "K-S":
        major = np.asarray([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        major = scipy.stats.zscore(major)

        minor = np.asarray([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        minor = scipy.stats.zscore(minor)

        major = scipy.linalg.circulant(major)
        minor = scipy.linalg.circulant(minor)

        if metric == "Pearson_correlation_coefficient":
            major = major.T.dot(summed_chroma)
            minor = minor.T.dot(summed_chroma)
        else:
            major = major.T
            minor = minor.T
            if metric == "laplacian_kernel":
                major = laplacian_kernel(major, np.asarray([summed_chroma])).reshape(-1)
                minor = laplacian_kernel(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "polynomial_kernel":
                major = polynomial_kernel(major, np.asarray([summed_chroma])).reshape(-1)
                minor = polynomial_kernel(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "cosine_similarity":
                major = cosine_similarity(major, np.asarray([summed_chroma])).reshape(-1)
                minor = cosine_similarity(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "abs_cosine_similarity":
                major = np.abs(cosine_similarity(major, np.asarray([summed_chroma])).reshape(-1))
                minor = np.abs(cosine_similarity(minor, np.asarray([summed_chroma])).reshape(-1))
            elif metric == "rbf_kernel":
                major = rbf_kernel(major, np.asarray([summed_chroma]), gamma=10).reshape(-1)
                minor = rbf_kernel(minor, np.asarray([summed_chroma]), gamma=10).reshape(-1)
            elif metric == "chi2_kernel":
                major = chi2_kernel(np.abs(major), np.abs(np.asarray([summed_chroma]))).reshape(-1)
                minor = chi2_kernel(np.abs(minor), np.abs(np.asarray([summed_chroma]))).reshape(-1)
            elif metric == "additive_chi2_kernel":
                major = additive_chi2_kernel(np.abs(major), np.abs(np.asarray([summed_chroma]))).reshape(-1)
                minor = additive_chi2_kernel(np.abs(minor), np.abs(np.asarray([summed_chroma]))).reshape(-1)
            elif metric == "euclidean_distances":
                major = euclidean_distances(major, np.asarray([summed_chroma])).reshape(-1) * -1.0
                minor = euclidean_distances(minor, np.asarray([summed_chroma])).reshape(-1) * -1.0
            elif metric == "entropy":
                mas = []
                mis = []
                for i in range(len(major)):
                    mas.append(-1.0 * entropy(major[i]**2, summed_chroma**2))
                    mis.append(-1.0 * entropy(minor[i]**2, summed_chroma**2))
                major = mas
                minor = mis
        max_major_idx = np.argmax(major)
        max_minor_idx = np.argmax(minor)

        if major[max_major_idx] >= minor[max_minor_idx]:
            key = (max_major_idx + 3) % 12
        else:
            key = (max_minor_idx + 3) % 12
            key += 12
        return key

    elif key_type == "binary":
        tonic = np.argmax(summed_chroma)

        major = np.asarray([1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 1.])
        major = scipy.stats.zscore(major)

        minor = np.asarray([1., 0., 1., 1., 0., 1., 0., 1., 1., 0., 1., 0.])
        minor = scipy.stats.zscore(minor)

        major = scipy.linalg.circulant(major)
        minor = scipy.linalg.circulant(minor)

        if metric == "Pearson_correlation_coefficient":
            major = major.T.dot(summed_chroma)
            minor = minor.T.dot(summed_chroma)
        else:
            major = major.T
            minor = minor.T
            if metric == "laplacian_kernel":
                major = laplacian_kernel(major, np.asarray([summed_chroma])).reshape(-1)
                minor = laplacian_kernel(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "polynomial_kernel":
                major = polynomial_kernel(major, np.asarray([summed_chroma])).reshape(-1)
                minor = polynomial_kernel(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "cosine_similarity":
                major = cosine_similarity(major, np.asarray([summed_chroma])).reshape(-1)
                minor = cosine_similarity(minor, np.asarray([summed_chroma])).reshape(-1)
            elif metric == "abs_cosine_similarity":
                major = np.abs(cosine_similarity(major, np.asarray([summed_chroma])).reshape(-1))
                minor = np.abs(cosine_similarity(minor, np.asarray([summed_chroma])).reshape(-1))
            elif metric == "rbf_kernel":
                major = rbf_kernel(major, np.asarray([summed_chroma]), gamma=10).reshape(-1)
                minor = rbf_kernel(minor, np.asarray([summed_chroma]), gamma=10).reshape(-1)
            elif metric == "chi2_kernel":
                major = chi2_kernel(np.abs(major), np.abs(np.asarray([summed_chroma]))).reshape(-1)
                minor = chi2_kernel(np.abs(minor), np.abs(np.asarray([summed_chroma]))).reshape(-1)
            elif metric == "additive_chi2_kernel":
                major = additive_chi2_kernel(np.abs(major), np.abs(np.asarray([summed_chroma]))).reshape(-1)
                minor = additive_chi2_kernel(np.abs(minor), np.abs(np.asarray([summed_chroma]))).reshape(-1)
            elif metric == "euclidean_distances":
                major = euclidean_distances(major, np.asarray([summed_chroma])).reshape(-1) * -1.0
                minor = euclidean_distances(minor, np.asarray([summed_chroma])).reshape(-1) * -1.0
            elif metric == "entropy":
                mas = []
                mis = []
                for i in range(len(major)):
                    mas.append(-1.0 * entropy(major[i]**2, summed_chroma**2))
                    mis.append(-1.0 * entropy(minor[i]**2, summed_chroma**2))
                major = mas
                minor = mis

        if major[tonic] >= minor[tonic]:
            key = (tonic + 3) % 12
        else:
            key = (tonic + 3) % 12
            key += 12
        return key



def new_accuracy_score(anses, preds):
    new_accuracy = 0
    for i in range(len(preds)):
        # same
        pr = preds[i]
        la = anses[i]
        if pr == la:
            new_accuracy += 1.
            continue

        # perfect-fifth error
        pr = preds[i]
        la = anses[i]
        if pr < 12 and la < 12:
            if (pr == (la + 7) % 12):
                new_accuracy += 0.5
                continue
        elif pr >= 12 and la >= 12:
            pr -= 12
            la -= 12
            if (pr == (la + 7) % 12):
                new_accuracy += 0.5
                continue

        # Relative major/minor
        pr = preds[i]
        la = anses[i]
        if pr < 12 and la >= 12:
            la -= 12
            if (pr == (la + 3) % 12):
                new_accuracy += 0.3
                continue
        elif pr >= 12 and la < 12:
            pr -= 12
            if ((pr + 3) % 12 == la):
                new_accuracy += 0.3
                continue

        # Parallel major/minor
        pr = preds[i]
        la = anses[i]
        if pr == (la + 12) % 24:
            new_accuracy += 0.2

    if len(anses) == len(preds):
        return new_accuracy / len(preds)
    else:
        print("Error!")



def calculate_and_report(gamma, CLP_func=0, key_type="K-S", genre="All_genres", metric="Pearson_correlation_coefficient"):
    preds = []
    anses = []
    if genre == "All_genres":
        with open("dataset/CLP_{}/chromas_gamma_{}.pickle".format(CLP_func, gamma), "rb") as CLPs:
            CLPs = pickle.load(CLPs)
        with open("dataset/CLP_{}/labels_gamma_{}.pickle".format(CLP_func, gamma), "rb") as labels:
            labels = pickle.load(labels)
    else:
        with open("dataset/CLP_{}/chromas_gamma_{}_{}.pickle".format(CLP_func, gamma, genre), "rb") as CLPs:
            CLPs = pickle.load(CLPs)
        with open("dataset/CLP_{}/labels_gamma_{}_{}.pickle".format(CLP_func, gamma, genre), "rb") as labels:
            labels = pickle.load(labels)

    for i in range(len(CLPs)):
        summed_chroma = np.sum(CLPs[i], axis=1)
        pred = finding_key(summed_chroma=summed_chroma, key_type=key_type, metric=metric)
        preds.append(pred)
        anses.append(labels[i])
    print("| {} | {} | {} | {} | {} | {:.3f} | {:.3f} |".format(genre, gamma, CLP_func, key_type, metric,
                                                   accuracy_score(anses, preds), new_accuracy_score(anses, preds)))



if __name__ == "__main__":
    for genre in genres:
        print("<center>Table of {}</center>".format(genre))
        print()
        print("| Genre | Gamma | CLP_func | Key_type | Metric | Acc | New_ACC |")
        print("| --- | --- | --- | --- | --- | --- |")
        for gamma in gammas:
            for CLP_func in CLP_methods:
                for metric in metrics:
                    for key_type in key_types:
                        calculate_and_report(gamma, CLP_func, key_type, genre, metric)
        print()

