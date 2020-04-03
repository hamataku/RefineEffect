import threading
import time
import pyaudio
import numpy as np
import struct


class SinWave():
    # settings
    INPUT = True
    OUT_FORMAT = pyaudio.paInt16
    IN_FORMAT = pyaudio.paFloat32
    RATE = 44100
    CHUNK = 1024

    L = 1
    R = 2
    LR = 3

    def __init__(self):
        self.pos = 0
        self.flagl = False
        self.flagr = False
        self.fvpp_list = [[0, 0, 0, 3]]
        self.stream_state = True

        self.pa = pyaudio.PyAudio()
        self.out_stream = self.pa.open(format=self.OUT_FORMAT,
                                       channels=2,
                                       rate=self.RATE,
                                       input=False,
                                       output=True,
                                       frames_per_buffer=self.CHUNK)
        self.thread = threading.Thread(target=self.output)
        self.thread.start()

        if self.INPUT:
            self.in_stream = self.pa.open(format=self.IN_FORMAT,
                                          channels=1,
                                          rate=self.RATE,
                                          input=True,
                                          output=False,
                                          frames_per_buffer=self.CHUNK)

    def output(self):
        while self.stream_state:
            data, self.pos = self.createData(
                self.fvpp_list, start_pos=self.pos)
            self.update(self.out_stream, data)

    def update(self, stream, data):  # 再生用関数、ストリームと波形データを引数に
        sp = 0  # 再生位置ポインタ
        buffer = data[sp:sp + self.CHUNK * 2]
        while buffer:
            stream.write(buffer)
            sp = sp + self.CHUNK * 2
            buffer = data[sp:sp + self.CHUNK * 2]

    def createData(self, fvpp, start_pos=0):  # オシレーター
        datal = []
        datar = []

        end_pos = start_pos + 0.05 * 44100
        for n in np.arange(start_pos, end_pos):
            sl = 0.0  # 波形データをゼロクリア
            sr = 0.0
            for f in fvpp:
                sl += np.sin(2 * np.pi * f[0] * n /
                             44100 + f[2]) * f[1] * (f[3] % 2)
                sr += np.sin(2 * np.pi * f[0] * n /
                             44100 + f[2]) * f[1] * (f[3] // 2)
                # 振幅が大きい時はクリッピング
                if sl > 1.0:
                    sl = 1.0
                    if self.flagl:
                        print("WARNING! Left Max Volume!!")
                        self.flagl = False
                if sr > 1.0:
                    sr = 1.0
                    if self.flagr:
                        print("WARNING! Right Max Volume!!")
                        self.flagr = False
                if sl < -1.0:
                    sl = -1.0
                if sr < -1.0:
                    sr = -1.0

            datal.append(sl)  # 末尾に追加
            datar.append(sr)
        datal = [int(x * 32767.0) for x in datal]  # 値を32767～-32767間にする
        datar = [int(x * 32767.0) for x in datar]
        s_data = np.array([datal, datar]).T.flatten()
        data = s_data.tolist()
        # バイナリに変換
        data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される

        return data, end_pos

    def play(self, freq, vol, phase, pan):
        self.fvpp_list.append([freq, abs(vol), phase, pan])
        self.flagl = True
        self.flagr = True

    def stop(self, freq):
        if freq in [row[0] for row in self.fvpp_list]:
            del self.fvpp_list[[row[0] for row in self.fvpp_list].index(freq)]
            return 0
        else:
            print("This frequency is not played!")
            return -1

    def input(self):
        ret = self.in_stream.read(self.CHUNK, exception_on_overflow=False)
        ret = np.fromstring(ret, np.float32)

        return ret

    def close(self):
        # スレッド停止
        self.stream_state = False
        self.thread.join()
        # streamの終了
        self.out_stream.stop_stream()
        self.out_stream.close()
        if self.INPUT:
            self.in_stream.stop_stream()
            self.in_stream.close()
        self.pa.terminate()
