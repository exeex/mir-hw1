
import os
import librosa


genres =['pop', 'blues', 'metal', 'rock', 'hiphop']

class Data():

    def __init__(self,genre,
                 au_path = "data/gtzan",
                 txt_path = "data/gtzan_key/gtzan_key/genres",):

        self.au_path = au_path
        self.txt_path = txt_path
        self.genre = genre

        au = os.listdir(os.path.join(au_path,genre))
        txt = os.listdir(os.path.join(txt_path,genre))
        au  = sorted(au)
        txt = sorted(txt)
        self.data = list(zip(au, txt))
        self.len = len(self.data)

    def __getitem__(self, idx):

        au_file, txt_file = self.data[idx]
        au_file = os.path.join(self.au_path,self.genre,au_file)
        txt_file = os.path.join(self.txt_path,self.genre,txt_file)

        au,sr = librosa.load(au_file)

        with open(txt_file, mode='r') as f:
            key = f.readline()
            key = int(key)

        return au, sr, key



d = Data('pop')
