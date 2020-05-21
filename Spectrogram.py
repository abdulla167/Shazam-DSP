from scipy.io import wavfile
import matplotlib.mlab as mlab
import matplotlib.pyplot as plot
import numpy as np
import imagehash
import librosa
import librosa.display
from librosa.core import load
import hashlib
from operator import itemgetter
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)



class Song():

    def __init__(self, path:"str" = ""):
        self.path = ""
        self.data = np.array([])
        self.sr = None
        self.spectrogram = np.array([])
        self.hash = ""
        if path == "":
            pass
        else:
            self.data, self.sr = load(path, mono=True, duration=60)

    def read_audio(self, path):
        self.data, self.sr = load(path, mono=True, duration=60)

    def get_spectrum(self):
        x = abs(librosa.core.stft(self.data, n_fft=1024))
        self.spectrogram = librosa.amplitude_to_db(x)

    def show_spectrogram(self):
        plot.figure(figsize=(15, 5))
        librosa.display.specshow(self.spectrogram, sr=self.sr)
        plot.colorbar(format='%+2.0f dB')
        plot.show()

    def get_hash(self):
        self.hash = imagehash.phash(self.spectrogram)

    def compare_hash(self,saved_hash:"str"):
        hamming_distaance = self.hash - saved_hash
        return hamming_distaance


    def get_2D_peaks(self, plot=False):
        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct,20)
        local_max = maximum_filter(self.spectrogram, footprint=neighborhood) == self.spectrogram
        background = (self.spectrogram== 0)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
        detected_peaks = local_max ^ eroded_background
        # extract peaks
        amps = self.spectrogram[detected_peaks]
        j, i = np.where(detected_peaks)
        # filter peaks
        amps = amps.flatten()
        peaks = zip(i, j, amps)
        peaks_filtered = filter(lambda x: x[2] > 10, peaks)  # freq, time, amp
        # get indices for frequency and time
        frequency_idx = []
        time_idx = []
        for x in peaks_filtered:
            frequency_idx.append(x[1])
            time_idx.append(x[0])
        return zip(frequency_idx, time_idx)



    def get_hashes(self):
        self.peak_hashes = []
        temp1 = self.get_2D_peaks()
        temp1 = sorted(temp1, key=lambda temp1: temp1[0])
        for i in range(len(temp1)):
            for j in range(1, 15):
                if (i + j) < len(temp1):
                    freq1 = temp1[i][1]
                    freq2 = temp1[i + j][1]
                    t1 = temp1[i][0]
                    t2 = temp1[i + j][0]
                    t_delta = t2 - t1
                    if 0 <= t_delta <= 200:
                        h = hashlib.sha1(("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))).encode('utf-8'))
                        self.peak_hashes.append((h.hexdigest()[0:20], int(t1)))









