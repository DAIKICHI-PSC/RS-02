# RS-02
Automatic Machine Control Software
RS-02 is software that can control inspection machines and robots with CNC-like programs without using PLC.
Interrupts and asynchronous processing are not supported.

I couldn't devote more time to development, so I released it.
We are actually operating 6 robots 24 hours a day.
I think it's good to use a multi-tap that cuts noise.

Requires Python 3.7.1 or higher and PySide6.
Maybe there are other libraries you need.
Please install if necessary.


24V compatible Arduino compatible machine (COMFILE Technology's FA-DUINO-24RA etc.) can input / output 24V (5V Arduino can also be used, but there is a possibility of malfunction due to noise).
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


2024/8/19 Use nuitka to make RS-02 faster.

nuitka --mingw64 --follow-imports  --onefile --standalone --enable-plugin=pyside6 RS02_MAIN.py

2024/9/10 Compatible with Keigan's KM-1U.
The thread will not terminate unless you change print("stop auto_serial_reading") to break in pykeigan's usbcontroller.py.

2025/3/19 Added virtual parallel processing. In addition to the program from the beginning, you can also virtually execute programs from the specified N number in parallel.




自動機制御ソフトウェア
RS-02は、検査機やロボットを、PLC使用せずにCNCライクなプログラムで制御出来るソフトウェアです。
割り込みや非同期処理には未対応となります。

これ以上開発に時間が割けなくなったので、公開しました。
実際に6台のロボットで24時間稼働させております。
ノイズをカットするマルチタップを使用するのが吉かと思います。

Python 3.7.1以上とPySide6が必要となります。
もしかしたら、他に必要なライブラリがあるかもしれません。
必要に応じてインストールして下さい。


24V対応のArduino互換機(COMFILE Technology社のFA-DUINO-24RA等)で24Vの入出力が可能（5VのArduinoも使用可能ですが、ノイズによる誤動作の可能性があります）。
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


2024/8/19 nuitkaを使用するとRS-02を高速に動作させる事が可能です。

nuitka --mingw64 --follow-imports  --onefile --standalone --enable-plugin=pyside6 RS02_MAIN.py

2024/9/10 Keigan社のKM-1Uに対応しました。
pykeiganのusbcontroller.pyにある、print("stop auto_serial_reading")をbreakに変更しないと、スレッドが終了しません。

2025/3/19 仮想並列処理を追加しました。先頭からのプログラムに加えて、指定したN番号からもプログラムを仮想的に並列実行出来ます。

