# -*- coding: utf-8 -*
import pyaudio
import wave

def main():
    audio = pyaudio.PyAudio()

    # 音声デバイス毎のインデックス番号を一覧表示
    for x in range(0, audio.get_device_count()):
        print(audio.get_device_info_by_index(x))

if __name__ == '__main__':
    main()
