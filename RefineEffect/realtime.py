import pyaudio
import numpy as np
import struct
from PyQt5 import QtWidgets, uic, QtCore
from realtime_form import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    OUTPUT_INDEX = 5
    INPUT_INDEX = 2
    CALIBRATE_PATH = "calibrate/earphone.npy"  # Calibrate earphone data
    LEFT_PATH = "earphone/L.npy"  # left poor earphone
    RIGHT_PATH = "earphone/R.npy"  # right poor earphone
    OUTPUT_FIX = 2  # change here according to sound level

    RATE = 44100  # サンプリング周波数
    OVERFLOW_LIMIT = 20480  # Inputのバッファーの閾値

    def __init__(self, parent=None):
        # pyqtのセットアップ
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # pyaudioセットアップ
        self.pa = pyaudio.PyAudio()
        self.out_stream = self.pa.open(format=pyaudio.paInt16,
                                       channels=2,
                                       rate=self.RATE,
                                       input=False,
                                       output=True,
                                       frames_per_buffer=1024,
                                       output_device_index=self.OUTPUT_INDEX)

        self.in_stream = self.pa.open(format=pyaudio.paInt16,
                                      channels=2,
                                      rate=self.RATE,
                                      input=True,
                                      output=False,
                                      frames_per_buffer=1024,
                                      input_device_index=self.INPUT_INDEX)

        # 測定データ(ndarray)読み込み
        calib = np.load(self.CALIBRATE_PATH)  # いい音イヤホン
        left = np.load(self.LEFT_PATH)  # 百均イヤホン右
        right = np.load(self.RIGHT_PATH)  # 百均イヤホン左

        self.FLAG = False  # ON/OFFのフラグ
        self.in_frames = 0
        self.out_frames = 0

        # 周波数ごとの倍率で最も大きい値を取得する
        max = np.max([calib / left, calib / right])
        # maxで割って倍率を０〜１の間に収める
        self.l_mag = calib / left / max
        self.r_mag = calib / right / max
        # FFT用に測定データを加工
        self.l_mag = np.append(
            np.append(self.l_mag, [0]), self.l_mag[:0:-1]) * self.OUTPUT_FIX
        self.r_mag = np.append(
            np.append(self.r_mag, [0]), self.r_mag[:0:-1]) * self.OUTPUT_FIX

        self.in_data = np.array([], dtype='int16')
        self.l_out = np.zeros(256, dtype='int16')
        self.r_out = np.zeros(256, dtype='int16')

        self.up = np.linspace(0, 1, 256)
        self.down = np.linspace(1, 0, 256)

        # タイマーセット
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def update(self):
        # インプットからのデータ読み込み
        if self.in_stream.get_read_available() >= 1024:
            input = self.in_stream.read(1024, exception_on_overflow=False)
            self.in_data = np.append(
                self.in_data, np.frombuffer(input, dtype='int16'))
            self.in_frames += 1024
        # インプットデータのフレーム数が1024を超えたら
        if self.in_frames >= 1024:
            left_data = self.in_data[:2047:2]
            right_data = self.in_data[1:2048:2]

            if self.FLAG:
                left_data = np.fft.ifft(np.fft.fft(
                    left_data) * self.l_mag).real.astype('int16')
                right_data = np.fft.ifft(np.fft.fft(
                    right_data) * self.r_mag).real.astype('int16')

            self.l_out[-256:] = self.l_out[-256:] * \
                self.down + left_data[0:256] * self.up
            self.r_out[-256:] = self.r_out[-256:] * \
                self.down + right_data[0:256] * self.up
            self.l_out = np.append(self.l_out, left_data[256:])
            self.r_out = np.append(self.r_out, right_data[256:])

            self.in_data = self.in_data[1536:]
            self.in_frames -= 768
            self.out_frames += 768

        # 出力データのフレーム数が1024を超えたら
        if self.out_frames >= 1024:
            data = np.array(
                [self.l_out[0:1024], self.r_out[0:1024]]).T.flatten()
            data = data.tolist()
            data = struct.pack("h" * len(data), *data)
            self.out_stream.write(data)
            self.l_out = self.l_out[1024:]
            self.r_out = self.r_out[1024:]
            self.out_frames -= 1024

        # オーバーフロー処理
        if self.in_frames > self.OVERFLOW_LIMIT:
            self.in_frames = 0
            self.out_frames = 0
            self.in_data = np.array([], dtype='int16')
            self.l_out = np.zeros(256, dtype='int16')
            self.r_out = np.zeros(256, dtype='int16')
            print("OVER FLOW!!")

    # ボタン操作で呼び出される関数
    def slot1(self):
        if self.FLAG:
            self.FLAG = False
        else:
            self.FLAG = True


if __name__ == '__main__':
    app = QtWidgets.QApplication([])  # アプリケーションを作成
    w = MainWindow()
    w.show()
    app.exec()
