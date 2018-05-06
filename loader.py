
import os
import librosa


genres =['pop', 'blues', 'metal', 'rock', 'hiphop']

class Data():

    def __init__(self, au_path = "data/gtzan",txt_path = "data/gtzan_key/gtzan_key/genres",
                 genres = genres):
        self.au_path = au_path
        self.txt_path = txt_path

        self.genres = genres
        self.genres_nb = len(genres)

        self.data = []
        for genre in genres:
            au = os.listdir(os.path.join(au_path,genre))
            txt = os.listdir(os.path.join(txt_path,genre))
            au  = sorted(au)
            txt = sorted(txt)
            file = zip(au, txt)
            self.data.append(list(file))

    def __getitem__(self, position):
        x, y = position

        au_file, txt_file = self.data[x][y]
        au_file = os.path.join(self.au_path,self.genres[x],au_file)
        txt_file= os.path.join(self.txt_path,self.genres[x],txt_file)

        au,sr = librosa.load(au_file)

        with open(txt_file, mode='r') as f:
            key = f.readline()
            key = int(key)

        print(au_file,txt_file)

        return au, sr, key



d = Data()
