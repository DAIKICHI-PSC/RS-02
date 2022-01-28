# RS-02
Easy Robot Maker


RS-02 is software that can control inspection machines and simple robots with CNC-like programs without using PLC.
Interrupts and asynchronous processing are not supported.

I couldn't devote more time to development, so I released it.
We are actually operating 5 robots 24 hours a day.
I think it's good to use a multi-tap that cuts noise.

Requires Python 3.7.1 or higher and PySide2.
Maybe there are other libraries you need.
Please install if necessary.


24V compatible Arduino compatible machine (Comfile's FA-DUINO24 etc.) can input / output 24V (5V Arduino can also be used, but there is a possibility of malfunction due to noise).
Change the port start number and the number of ports of the firmware "PLC-01.ino" depending on the model.
Depending on the input value, the program processing can be branched.
Connect with RS232C.

Compatible with SUS's single-axis robot XA series (teaching only).
Compatible with IAI's single-axis robot RCP series (position specification only).
Asynchronous operation of multiple axes is possible.
Connect with RS232C.

Compatible with measuring instruments that can receive measured values with RS232C.
By specifying the tolerance range and judging OK and NG, the program processing can be branched.

Up to 100 devices can be connected to each device.


Execute "RS02_MAIN.py".
To run the program, load the program (text file) in "EDIT" mode and press the "RUN" button in "AUTO" mode to run it.
See "RS-02 USERS MANUAL.docx" for instruction details. 


RS-02は、P検査機や簡易的なロボットを、PLC使用せずにCNCライクなプログラムで制御出来るソフトウェアです。
割り込みや非同期処理には未対応となります。

これ以上開発に時間が割けなくなったので、公開しました。
実際に5台のロボットで24時間稼働させております。
ノイズをカットするマルチタップを使用するのが吉かと思います。

Python 3.7.1以上とPySide2が必要となります。
もしかしたら、他に必要なライブラリがあるかもしれません。
必要に応じてインストールして下さい。


24V対応のArduino互換機(Comfile社のFA-DUINO24等)で24Vの入出力が可能（5VのArduinoも使用可能ですが、ノイズによる誤動作の可能性があります）。
機種により、ファームウェア「PLC-01.ino」のポート開始番号とポート数を変更してください。
入力値により、プログラム処理の分岐が出来ます。
RS232Cで接続します。

SUS社の単軸ロボットXAシリーズに対応（ティーチングのみ）。
IAI社の単軸ロボットRCPシリーズに対応（位置指定のみ）。
複数軸の非同期動作が可能です。
RS232Cで接続します。

RS232Cで測定値が受け取れる測定器に対応。
公差範囲を指定して、OKとNGの判定により、プログラム処理の分岐が出来ます。

各機器は各100台まで接続可能となってます。


「RS02_MAIN.py」を実行して下さい。
プログラムを動作させるには、「EDIT」モードでプログラム(テキストファイル)を読み込み、「AUTO」モードで「RUN」ボタンを押して実行します。
命令の詳細は「RS-02 USERS MANUAL.docx」を参照してください。
