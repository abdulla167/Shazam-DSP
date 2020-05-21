from last_gui im
import sys
from PyQt5 import QtWidgets
from Spectrogram import Song
import xlsxwriter
import os
import xlrd
import numpy as np
from imagehash import hex_to_hash
import json
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)

class ApplicationWindow(QtWidgets.QMainWindow):
    hamming_distance = np.array([])
    song1 = Song()
    song2 = Song()
    mixed_song = Song()

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(lambda : self.load_song(1))
        self.ui.pushButton_4.clicked.connect(lambda :self.load_song(2))
        self.ui.pushButton_2.clicked.connect(self.mix)
        self.ui.pushButton.clicked.connect(self.match_hash_peaks)
        self.form_widget = MyTable(10, 1)
        self.read_songs("F:/3rd year/DSP/task4/Songs")

    def get_slider_value(self):
        value = self.ui.horizontalSlider.value()
        return value

    def read_songs(self, path):
         if os.stat("data.json").st_size == 0 :
            workbook = xlsxwriter.Workbook('hello.xlsx')
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Hash')
            worksheet.write('C1', 'Song_path')
            i = 1
            dict = {}
            for filename in os.listdir(path):
                if filename.endswith(".mp3"):
                    current_path = os.path.join(path, filename)
                    print(current_path)
                    song = Song(current_path)
                    song.get_spectrum()
                    song.get_hashes()
                    dict.update({filename: song.peak_hashes})
                    print(song.hash)
                    print(dict[filename])
                    worksheet.write(i, 0, str(song.hash))
                    worksheet.write(i, 2, str(current_path))
                    i += 1
                else:
                    continue
            workbook.close()
            with open('data.json', 'w') as fp:
                json.dump(dict, fp)

    def load_song(self,x):
        song_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song", "~", "Songs ( *.wav *.mp3 )")
        if x== 1:
            self.song1.read_audio(song_path[0])
            self.mixed_song.data = np.copy(self.song1.data)
        elif x==2:
            self.song2.read_audio(song_path[0])
            self.mixed_song.data = np.copy(self.song2.data)



    def mix(self):
        slider_value = self.get_slider_value()/100
        self.mixed_song.data = (self.song1.data * slider_value) + (self.song2.data * (1- slider_value))
        self.mixed_song.sr = self.song1.sr
        self.mixed_song.get_spectrum()
        self.mixed_song.get_hash()
        self.mixed_song.get_hashes()


    def match_hash_peaks(self):
        similarity = []
        with open('data.json') as f:
            data = json.load(f)
        for key in data:
            current_song = set(np.array(data[key])[:,0])
            intersect = current_song.intersection(set(np.array(self.mixed_song.peak_hashes)[:,0]))
            similarity.append([len(intersect),key])
        similarity = sorted(similarity, key=lambda similarity: similarity[0])
        similarity = similarity[::-1]
        for x in range(10):
            self.form_widget.setItem(x, 0, QTableWidgetItem(similarity[x][1]))
        self.form_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.form_widget.setHorizontalHeaderLabels(['Name'])
        self.form_widget.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()

    app.exec_()


if __name__ == "__main__":
    main()
