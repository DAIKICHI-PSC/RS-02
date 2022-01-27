# RS-02
Easy Robot Maker

検査機や簡易的なロボットを、ＣＮＣライクなプログラムで制御出来るソフトウェアです。
割り込みや非同期処理には未対応となります。

これ以上開発に時間が割けなくなったので、公開しました。
実際に5台のロボットで24時間稼働させております。
ノイズをカットするマルチタップを使用するのが吉かと思います。

Python 2.7.1以上 PySideが必要となります。


24V対応のArduino互換機(Comfile社のFA-DUINO24等)で24Vの入出力が可能。
機種により、ファームウェア「PLC-01.ino」のポート開始番号とポート数を変更してください。
入力値により、プログラム処理の分岐が出来ます。

SUS社の単軸ロボットXAシリーズに対応（ティーチングのみ）。
IAI社の単軸ロボットRCPシリーズに対応（位置指定のみ）。
複数軸の非同期動作が可能です。

RS232Cで測定値が受け取れる測定器に対応。
公差範囲を指定して、OKとNGの判定により、プログラム処理の分岐が出来ます。

各機器は各100台まで接続可能となってます。


動作させるには、「EDIT」モードでプログラム(テキストファイル)を読み込み、「AUTO」モードで「RUN」ボタンを押して実行します。
命令の詳細は「RS-02 USERS MANUAL.docx」を参照してください。
