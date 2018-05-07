import os
import librosa
import torch
from torch.utils.data import Dataset
import numpy as np

genres = ['pop', 'blues', 'metal', 'rock', 'hiphop']


class Song:

    def __init__(self, wav_path, window=10):

        self.wav_path = wav_path
        self.data, self.sr = librosa.load(self.wav_path)
        self.shape = self.data.shape
        self.time = self.shape[0] / self.sr

        transform = self.chroma

        if transform:
            self.data = transform(self.data)

            self.window = window
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
        return np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y=au, sr=sr, n_fft=4096, hop_length=22050)))


class Song2:

    def __init__(self, wav_path, window=10):

        self.wav_path = wav_path
        self.data, self.sr = librosa.load(self.wav_path)
        self.shape = self.data.shape
        self.time = self.shape[0] / self.sr

    def chroma(self, au, sr=22050, gamma=10):
        return np.log(1 + gamma * np.abs(librosa.feature.chroma_stft(y=au, sr=sr, n_fft=4096, hop_length=22050)))