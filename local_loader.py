import os
import librosa
import torch
from torch.utils.data import Dataset
import numpy as np

genres = ['pop', 'blues', 'metal', 'rock', 'hiphop']

key_map = {
    "A": 0,
    "A+": 1,
    "B-": 1,
    "B": 2,
    "C": 3,
    "C+": 4,
    "D-": 4,
    "D": 5,
    "D+": 6,
    "E-": 6,
    "E": 7,
    "F": 8,
    "F+": 9,
    "G-": 9,
    "G": 10,
    "G+": 11,
    "A-": 11,
    "a": 12,
    "a+": 13,
    "b-": 13,
    "b": 14,
    "c": 15,
    "c+": 16,
    "d-": 16,
    "d": 17,
    "d+": 18,
    "e-": 18,
    "e": 19,
    "f": 20,
    "f+": 21,
    "g-": 21,
    "g": 22,
    "g+": 23,
    "a-": 23,
}


class Song:

    def __init__(self, wav_path, window=10):

        self.wav_path = wav_path
        self.data, self.sr = librosa.load(self.wav_path)
        self.shape = self.data.shape
        self.time = self.shape[0] / self.sr

        transform = self.chroma
        self.window = window

        if transform:
            self.data = transform(self.data)
            pad_size = (self.window + 1) // 2
            self.data = np.pad(self.data, [(0, 0), (pad_size, pad_size)], 'constant', constant_values=(0, 0))
            self.shape = self.data.shape

    def __len__(self):
        return self.data.shape[1]

    def __getitem__(self, i):
        l = len(self)
        if i < l - self.window + 1 - self.window % 2:
            return self.data[:, i:i + self.window]
        else:
            raise IndexError


    def chroma(self, au, sr=22050, gamma=10):
        return np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y=au, sr=sr, n_fft=4096, hop_length=self.sr)))


class Data():

    def __init__(self,
                 au_path="data/BPS_piano",
                 txt_path="data/BPS_txt",
                 window=10, ):
        self.au_path = au_path
        self.txt_path = txt_path

        au = os.listdir(au_path)
        txt = os.listdir(txt_path)
        au = sorted(au)
        txt = sorted(txt)
        self.data = list(zip(au, txt))
        self.window = window

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        au_file, txt_file = self.data[idx]
        au_file_path = os.path.join(self.au_path, au_file)
        txt_file_path = os.path.join(self.txt_path, txt_file)

        s = Song(au_file_path, window=self.window)

        keys = []
        with open(txt_file_path, mode='r') as f:

            time = -1
            for line in f.readlines():
                if time == int(line.split('\t')[0]):
                    continue
                time = int(line.split('\t')[0])

                key = line.split('\t')[1].replace('\n', '')
                keys.append(key_map[key])

        return s, keys, au_file_path, txt_file


d = Data()