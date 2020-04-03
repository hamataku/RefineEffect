# Refine Effect（百均イヤホン高音質化ツール）

### English Explanation is [here!](https://github.com/hamataku/RefineEffect/blob/master/README.md)

"Refine Effect"は百均イヤホンの音質を向上させることができるツールです。

## 説明

イヤホンは安かろう悪かろう。どうしてでしょうか。
僕が思うにイヤホンの周波数特性が異常に悪いためです。当たり前か

だから、普通のマイクを使ってイヤホンの周波数特性を測って、イヤホンの出音がフラットな周波数特性になるように元の音源をいじってやれば、良い音が出てくるはず。この仮説のもとそれを実現するツールを作りました。

マイクの周波数特性を知る必要はありませんが、その代わりに音質がいいイヤホンが必要です。このツールは良音イヤホンのデータと百均イヤホンのデータを比べて、周波数ごとの倍率を決定します。つまりは、百均イヤホンを良音イヤホンにできるだけ近づけると言うことです。

## デモ

このリポジトリには二つのツールが入っています。
一つ目(main.py) はイヤホンの周波数特性を測定するためのツールです。

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/4.gif)

二つ目(realtime.py)はパソコンの音声出力を仮想オーディオインターフェースによって取り込んで、リアルタイムで百均イヤホンに合わせた音を生成するツールです。  
シンプルイズベスト。

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/2.png)

## 環境

以下の環境でこのツールを開発しました。

    $ python -V
    Python 3.6.5 :: Anaconda, Inc.

## 必要事項

以下のPythonパッケージを必要とします。

-   numpy  
-   PyQt5  
-   pyaudio  
-   threading  

そして仮想オーディオインターフェースをインストールする必要があります。
下記のソフトは動作確認済みです。

-   Soundflower(Mac)  
-   VB-CABLE(Windows)  

あとは長ったらしい「使い方」を読み進める**パッション**があれば尚のことヨシです。

## 使い方

1. RefineEffectのディレクトリに移動し、以下のコードをコマンドラインで実行して下さい。

    $ python main.py

そして、良音イヤホンの片耳（どちらでも良い）と百均イヤホンの両耳を測定して下さい。ファイル名は適宜。

2. 出力オーディオデバイスの変更
Macユーザーは、設定->サウンド->出力->"Soundflower(2ch)"を選択

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/3.png)

Windowsユーザーは、設定->サウンド->再生->"CABLE Input"を選択

![demo](https://github.com/hamataku/RefineEffect/blob/master/requests/6.png)

3. device indexの確認
以下のコードを実行して下さい。

    $ python device.py

Macユーザーは、出力として"Built-in Output"、入力として"Soundflower(2ch)"の番号を確認。
Windowsユーザーは、出力として"CABLE Output"、入力は環境によって異なるので適宜。

4. realtime.pyの編集

下記の変数を自分の環境に合わせて書き換えて下さい。

```Python
class MainWindow(QtWidgets.QMainWindow):
    OUTPUT_INDEX = 3
    INPUT_INDEX = 4
    CALIBRATE_PATH = "calibrate/earphone.npy"  # Calibrate earphone data
    LEFT_PATH = "earphone/L.npy"  # left poor earphone
    RIGHT_PATH = "earphone/R.npy"  # right poor earphone
    OUTPUT_FIX = 7  # Change here according to sound level
```

5. リアルタイムイコライザーの実行

    $ python realtime.py

あとは百均イヤホンで良音をお楽しみ下さい。

## トラブルシューティング

### ノイズがすごい。音割れする。
realtime.pyの中の`OUTPUT_FIX`の値を小さくしてみて下さい。

### 音が小さすぎる
realtime.pyの中の`OUTPUT_FIX`の値を大きくしてみて下さい。

## ウェブサイト

[HatenaBlog](https://hamatakuzaq.hateblo.jp/entry/2020/03/09/111850)

## ライセンス

[MIT](https://github.com/hamataku/RefineEffect/blob/master/LICENSE)

## 作者

[Taku Hamazaki](https://twitter.com/Warapen4)
