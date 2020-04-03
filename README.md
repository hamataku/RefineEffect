# Refine Effect（百均イヤホン高音質化ツール）

### 日本語説明は[こちら](https://github.com/hamataku/RefineEffect/blob/master/README_JP.md)

"Refine Effect" is a tool which can improve sound quality of cheap earphones.

## Description

Most cheap earphones have poor sound quality. Why?  
In my opinion, it is because they don't have flat frequency characteristics.  

Therefore, I decided to develop a tool to measure them and make the untidy characteristics flat using a normal microphone.  

You don't have to know the microphone's frequency characteristics, but you need a good earphone.  
This tool compares cheap earphones's data with good earphone's data, and calculates magnifications with respect to each frequency. In other words, it makes your cheap earphone closer to your good earphone.

## Demo

This repository contains two different tools.  
The former(main.py) measures frequency characteristics of your earphones.

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/4.gif)

The latter(realtime.py) takes in audio output of your PC and reproduces good sound tuned for your cheap earphones in real time.

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/2.png)

## Environment

I developed these tools in the environment as shown below.

    $ python -V
    Python 3.6.5 :: Anaconda, Inc.

## Requirement

This tool requires following Python packages.

-   numpy  
-   PyQt5  
-   pyaudio  
-   threading  

And you have to install a virtual audio driver.
I confirmed following softwares works well.

-   Soundflower(Mac)  
-   VB-CABLE(Windows)  

## Usage

1. Move to the RefineEffect directory and execute a frequency measuring tool.

    $ python main.py

Measure your good earphone once, and then measure both side of your cheap earphone.

2. change output device.  
If you use Mac, setting->sound->output->select "Soundflower(2ch)".

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/3.png)

If you use Windows, setting->sound->playback->select "CABLE Input".

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/6.png)

3. Check both output and input device index.

    $ python device.py

If you use Mac, output device is "Built-in Output" and input device is "Soundflower(2ch)".  
If you use Windows, output device is "CABLE Output" and input device depends on your environment.  

4. Edit realtime.py  
Change these variables to suit your environment.
```Python
class MainWindow(QtWidgets.QMainWindow):
    OUTPUT_INDEX = 3
    INPUT_INDEX = 4
    CALIBRATE_PATH = "calibrate/earphone.npy"  # Calibrate earphone data
    LEFT_PATH = "earphone/L.npy"  # left poor earphone
    RIGHT_PATH = "earphone/R.npy"  # right poor earphone
    OUTPUT_FIX = 7  # Change here according to sound level
```

5. Execute a real-time equalizer.

    $ python realtime.py

Enjoy good sound!

## Trouble shooting

### Too noisy
Decrease the number of `OUTPUT_FIX` in realtime.py.

### Too soft
Increase the number of `OUTPUT_FIX` in realtime.py.

## Website

[HatenaBlog](https://hamatakuzaq.hateblo.jp/entry/2020/03/09/111850)

## Licence

[MIT](https://github.com/hamataku/RefineEffect/blob/master/LICENSE)

## Author

[Taku Hamazaki](https://twitter.com/Warapen4)
