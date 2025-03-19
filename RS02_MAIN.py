#-*- coding: utf-8 -*-

#####2025/3/19 Changed so that M21 and M22 can work properly for each virtual paralell process
#####Refer to comment CNG4

#####2025/3/11 Changed so that M200 can operate in each virtual paralell process
#####Refer to comment CNG3

#####2025/3/10 Display option of virtual paralell process added
#####Refer to comment CNG2

#####2025/3/7 Virtual paralell process added
#####Refer to comment CNG1


import os
import sys
import time
import threading
import re
import serial
import serial.tools.list_ports
from PySide6 import QtCore, QtGui, QtWidgets
from RS02_GUI import Ui_MainWindow #QT Designerで作成し変換したファイルの読込

from pykeigan import usbcontroller
from pykeigan import utils

from MODBUS_ASCII_LRC import LRC_CREATE, LRC_CHECK
from MODBUS_ASCII_CONVERTERS import DECIMAL_TO_HEX, RESPONSE_TO_BYTES
#from VALUE_CHECKER import DIGIT_CHK
#import DobotDllType as dType




















#####グローバル変数#######################################################################################
MOVE_TIME_OUT = 10 #####Ｄｏｂｏｔ移動タイムアウト確認用（経過時間上限値）
TOLORANCE = 0.2 #####設定公差
OVERRIDE_VAL = 0.1 #####オーバーライド値
RAPPID_VAL = 25 #####スピード値
AOTO_MODE_STAT = 0 #####AUTOモードの状態
ERROR_DETECT = 1 #####マルチスレッドかシングルスレッドかの確認用
THREAD_LOCK = threading.Lock() 
INSTRUMENT_CURRENT_VAL = 0 #####測定器現在値記憶用変数
RCP_POS_DIFF = 0.1 #####RCP軸位置決精度を記憶する関数
#####Ｄｏｂｏｔを配列化
#api = []
#for i in range(0,101):
    #api.append(dType.load())
#####
#####測定器用にシリアル通信関数を配列化
LIST_INSTRUMENT = []
for i in range(0, 101):
    LIST_INSTRUMENT.append(serial.Serial)
#####
#####PLC用にシリアル通信関数を配列化
LIST_PLC = []
for i in range(0, 101):
    LIST_PLC.append(serial.Serial)
#####
#####XA用にシリアル通信関数を配列化
LIST_XA = []
for i in range(0, 101):
    LIST_XA.append(serial.Serial)
#####
#####RCP用にシリアル通信関数を配列化
LIST_RCP = []
for i in range(0, 101):
    LIST_RCP.append(serial.Serial)
#####
#####KM-1U用にシリアル通信関数を配列化
LIST_KM = []
for i in range(0, 101):
    LIST_KM.append(usbcontroller.USBController)
#####


#####各種配列#######################################################################################
DICT_MACHINE_WORK_STAT = {} #####各機動作状況確認用辞書
DICT_MACHINE_FIN_STAT = {} #####マルチスレッド時の動作完了状況確認用辞書
DICT_INSTRUMENT_PARAM = {} #####測定機器パラメータ保存用辞書
DICT_VARIABLE = {} #####プログラム内変数用辞書
#####
#####カウンター関連
LOOP_COUNT = 0
NG_VAL = 0
H_FAIL_VAL = 0
H_FAIL_COUNTER = 0
#####
#####その他
Debug_Mode = 0 #####デバッグモード用フラグ
#####




















####################################################################################################################################################################
####################################################################################################################################################################
#################################メインループ処理####################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
#####関数########################################
#####AUTOモード用関数
def RUN_RS():
    global AOTO_MODE_STAT
    global DICT_MACHINE_WORK_STAT
    global DICT_INSTRUMENT_PARAM
    global DICT_VARIABLE
    global ERROR_DETECT
    global LOOP_COUNT
    global H_FAIL_VAL
    global H_FAIL_COUNTER
    global MOVE_TIME_OUT
    global RCP_POS_DIFF
    global NG_VAL

    DICT_MACHINE_WORK_STAT.clear()
    DICT_MACHINE_FIN_STAT.clear()
    DICT_INSTRUMENT_PARAM.clear()
    DICT_VARIABLE.clear()
    ERROR_DETECT = 1

    Nc_Command = "" #####命令一時格納用
    Nc_val = "" #####命令値一時格納用
    #selectedDobot = -1 #####選択されたＤｏｂｏｔ名格納用
    SelectedPLC = -1 #####選択されたPLC名格納用
    SelectedXA = -1 #####選択されたXA名格納用  
    SelectedRCP = -1 #####選択されたRCP名格納用
    SelectedKM = -1 #####選択されたKM-1U名格納用

    #CNG1_2
    #CNG4_1
    VirtualValue = [[0, -1, -1, -1, -1, 1]] #仮想並列処理の各値 [[Current_Line_Number, SelectedPLC, SelectedXA, SelectedRCP, SelectedKM, ERROR_DETECT], []]
    #CNG4_1
    VirtualNum = 0 #仮想並列処理の総数
    VirtualCurrentNum = 0 #仮想並列処理の現在の処理番号
    #CNG1_2

    #CNG2_1
    VirtualDisplay = -1
    #CNG2_1

    #CNG3_1
    VirtualMachine = [[]] #各仮想並列処理で受け持つ機器を登録し、M200で受け持つ機器のみを確認（各処理のM200でクリア）
    #CNG3_1

    #FeedRate = 10
    Timer = 0
    TimeOut = 0
    ElapsedTime = 0
    #DSerial = {} #####各機シリアルポート記憶用辞書
    Dict_Machine_Name_Num = {} #####各機器個体識別用辞書（配列内値例：["D1", 1]） 値はシリアル通信用配列で使用
    Dict_Jump_Distination_Num = {} #####プログラムのジャンプ先行番号記憶用辞書（配列内値例：["P1", 15]）




















    ##################################################################################
    ##################################################################################
    ##############################セッティングの確認と設定##############################
    ##################################################################################
    ##################################################################################
    isError = 1 #####設定チェックループでエラー発生の確認
    Total_Line_Number = win.ui.plainTextEdit_1.blockCount() #####plainTextEdit_1の行数を取得
    Current_Line_Number = 0 #####現在の行番号
    win.ui.plainTextEdit_2.clear()
    WConsole(">CHECKING SETTINGS...")
    while(True):

        #####指定行を取得
        PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
        win.ui.plainTextEdit_1.moveCursor(QtGui.QTextCursor.End) #####指定した行へ移動
        cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number)) #####指定した行へ移動
        win.ui.plainTextEdit_1.setTextCursor(cursor) #####指定した行へ移動
        cursor = win.ui.plainTextEdit_1.textCursor() #####選択範囲をハイライト表示する
        cursor.movePosition(QtGui.QTextCursor.EndOfBlock, QtGui.QTextCursor.KeepAnchor, 1) #####選択範囲をハイライト表示する
        win.ui.plainTextEdit_1.setTextCursor(cursor) #####選択範囲をハイライト表示する
        win.ui.plainTextEdit_1.setFocus
        app.processEvents() #####ループ中もプロセスが動作する様にする
        time.sleep(float(win.ui.comboBox_2.currentText()))
        #####


        #========================================Nコマンド用　ジャンプ先の位置（行）========================================
        #PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
        if(PText.startswith("N") == True):
            Nc_Command = PText.replace("N", "") #####Nc_Commandの文字列から"N"を削除
            if(Nc_Command.isdigit() == False):
                WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                break
            else:
                Dict_Jump_Distination_Num["P" + Nc_Command] = Current_Line_Number #####Nが記述されている行番号を記憶
                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                    WConsole("N"  +Nc_Command + " : Line " + str(Current_Line_Number) + ".")
        #####


        #========================================SETコマンド用　各機器の設定========================================
        elif(PText.startswith("SET ") == True): #####PTextの文字列の先頭が"SET "で始まるか確認
            PText = PText.replace("SET ", "") #####PTextの文字列から"SET "を削除
            #####Aコマンド用
            if(PText.startswith("A") == True): #####PTextの文字列の先頭が"A"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    Machine_Number = Nc_Command.replace("A", "") #####命令の数字部分のみを取得
                    Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    elif(int(Machine_Number) > 100):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        break
                    elif((Nc_val in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        break
                    else:
                        Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にXコマンドと配列番号を登録
                        #DSerial[Nc_Command] = Nc_val #####辞書に登録
                        DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にXコマンドと実行結果を登録
                        DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にXコマンドと動作状況を登録
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole("SET :" +  Nc_Command + " is " + Nc_val + ".")
                        ret = AConnect(Nc_val, Dict_Machine_Name_Num[Nc_Command])
                        if(ret > 0):
                            break
                        else:
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val + " succeed.")
                            time.sleep(0.1)
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


            #========================================Bコマンド用========================================
            if(PText.startswith("B") == True): #####PTextの文字列の先頭が"B"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    Machine_Number = Nc_Command.replace("B", "") #####命令の数字部分のみを取得
                    Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    elif(int(Machine_Number) > 100):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        break
                    elif((Nc_val in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        break
                    else:
                        Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にXコマンドと配列番号を登録
                        #DSerial[Nc_Command] = Nc_val #####辞書に登録
                        DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にXコマンドと実行結果を登録
                        DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にXコマンドと動作状況を登録
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole("SET :" +  Nc_Command + " is " + Nc_val + ".")
                        ret = BConnect(Nc_val, Dict_Machine_Name_Num[Nc_Command])
                        if(ret > 0):
                            break
                        else:
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val + " succeed.")
                            time.sleep(0.1)
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


            #========================================Dコマンド用========================================
            #elif(PText.startswith("D") == True): #####PTextの文字列の先頭が"D"で始まるか確認
                #if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    #Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    #Machine_Number = Nc_Command.replace("D", "") #####命令の数字部分のみを取得
                    #Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    #if(Nc_val == ""): #####Nc_valに値があるか確認
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        #break
                    #elif(Machine_Number.isdigit() == False):
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        #break
                    #elif(int(Machine_Number) > 100):
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        #break
                    #elif((Nc_val in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        #break
                    #else:
                        #Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にDコマンドと配列番号を登録
                        #DSerial[Nc_Command] = Nc_val #####辞書に登録
                        #DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にDコマンドと実行結果を登録
                        #DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にDコマンドと動作状況を登録
                        #if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            #WConsole("SET :" +  Nc_Command + " is " + Nc_val + ".")
                        #ret = DConnect(Nc_val, Dict_Machine_Name_Num[Nc_Command])
                        #if(ret > 0):
                            #break
                        #else:
                            #if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                #WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val + " succeed.")
                            #time.sleep(0.1)
                #else:
                    #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    #break
            #####


            #========================================Hコマンド用========================================
            elif(PText.startswith("H") == True): #####PTextの文字列の先頭が"H"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Nc_val.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    else:
                        H_FAIL_VAL = int(Nc_val)
                        H_FAIL_COUNTER = H_FAIL_VAL
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole("SET : H is " + str(H_FAIL_VAL) + ".")
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


            #========================================Iコマンド用　測定器の設定========================================
            if(PText.startswith("I") == True): #####PTextの文字列の先頭が"I"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    Machine_Number = Nc_Command.replace("I", "") #####命令の数字部分のみを取得（機器番号）
                    Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    Nc_val_List = [] #####取得した値を配列に記憶(COMポート, ボーレート, バイトサイズ, パリティー, ストップビット, 取得データ内の測定値開始位置, 取得データ内の測定値終了位置, 上限値, 下限値)
                    Nc_val_List = Nc_val.split(",")
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    elif(int(Machine_Number) > 100):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        break
                    elif(len(Nc_val_List) < 10):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need 10 parameters.")
                        break
                    elif((Nc_val_List[0] in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        break
                    else:
                        sPos = Nc_val_List[6]
                        ePos = Nc_val_List[7]
                        maxValue = Nc_val_List[8] #最大値が数値か確認する為の変数
                        TMPmaxValue = maxValue.replace("+", "")
                        TMPmaxValue = TMPmaxValue.replace("-", "")
                        TMPmaxValue = TMPmaxValue.replace(".", "")
                        minValue = Nc_val_List[9] #最小値が数値か確認する為の変数
                        TMPminValue = minValue.replace("+", "")
                        TMPminValue = TMPminValue.replace("-", "")
                        TMPminValue = TMPminValue.replace(".", "")
                        if(sPos.isdigit() == False):
                            WConsole("ERROR : Start position is not digit.")
                            break
                        elif(ePos.isdigit() == False):
                            WConsole("ERROR : End position is not digit.")
                            break
                        elif(TMPmaxValue.isdigit() == False):
                            WConsole("ERROR : Max Tolorance is not digit.")
                            break
                        elif(TMPminValue.isdigit() == False):
                            WConsole("ERROR : Minimum Tolorance is not digit.")
                            break
                        elif(int(sPos) > int(ePos)):
                            WConsole("ERROR : Stat position must not be greater than end position.")
                            break
                        else:
                            Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にIコマンドと配列番号を登録
                            #DSerial[Nc_Command] = Nc_val #####辞書に登録
                            DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にIコマンドと実行結果を登録
                            DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にIコマンドと動作状況を登録
                            DICT_INSTRUMENT_PARAM[Nc_Command] = Nc_val #####辞書にIコマンドとパラメータを登録
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole("SET :" +  Nc_Command + " is " + Nc_val_List[0] + ".")
                            ret = IConnect(Nc_Command, Dict_Machine_Name_Num[Nc_Command])
                            if(ret > 0):
                                break
                            else:
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val_List[0] + " succeed.")
                                time.sleep(0.1)
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


            #CNG1_3
            #========================================Vコマンド用　仮想並列処理の設定========================================
            elif(PText.startswith("V") == True): #####PTextの文字列の先頭が"V"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    #CNG2_2
                    Machine_Number = Nc_Command.replace("V", "") #####命令の数字部分のみを取得
                    Machine_Number_B = Machine_Number.replace("-", "") #####命令の数字部分のみを取得
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number_B.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    else:
                        VirtualDisplay = int(Machine_Number)
                        v = Nc_val.split(',')
                        v_len = len(v)
                        if(VirtualDisplay > v_len):
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Value of V is too big.")
                            break
                        elif(VirtualDisplay < -1):
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Value of V is too small.")
                            break
                            #CNG2_2
                        for i in v:
                            if(("N" in i) == False):
                                WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need N value.")
                                break
                            l = i.replace("N", "")
                            if(l.isdigit() == False):
                                WConsole("ERROR : Need digit after N.")
                                break
                            i = i.replace("N", "P")
                            #CNG4_4
                            VirtualValue.append([i, -1, -1, -1, -1, 1])
                            #CNG4_4
                            #CNG3_2
                            VirtualMachine.append([])
                            #CNG3_2
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####
            #CNG1_3


            #========================================Lコマンド用　PLCの設定========================================
            elif(PText.startswith("L") == True): #####PTextの文字列の先頭が"L"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    Machine_Number = Nc_Command.replace("L", "") #####命令の数字部分のみを取得
                    Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    elif(int(Machine_Number) > 100):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        break
                    elif((Nc_val in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        break
                    else:
                        Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にLコマンドと配列番号を登録
                        #DSerial[Nc_Command] = Nc_val #####辞書に登録
                        DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にLコマンドと実行結果を登録
                        DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にLコマンドと動作状況を登録
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole("SET :" +  Nc_Command + " is " + Nc_val + ".")
                        ret = LConnect(Nc_val, Dict_Machine_Name_Num[Nc_Command])
                        if(ret > 0):
                            break
                        else:
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val + " succeed.")
                            time.sleep(0.1)
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


            #========================================Oコマンド用　KM-1Uの設定========================================
            elif(PText.startswith("O") == True): #####PTextの文字列の先頭が"O"で始まるか確認
                if(("=" in PText) == True): #####PTextの文字列に"="が含まれるか確認
                    Nc_Command, Nc_val = PText.split("=") #####PTextの文字列を"="で分割し、Nc_CommandとNc_valに代入
                    Machine_Number = Nc_Command.replace("O", "") #####命令の数字部分のみを取得
                    Serial_Number = Check_Serial() #####存在するシリアルポートを取得
                    if(Nc_val == ""): #####Nc_valに値があるか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number or value.")
                        break
                    elif(Machine_Number.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    elif(int(Machine_Number) > 100):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number should be under 100.")
                        break
                    elif((Nc_val in Serial_Number) == False): #####実際のシリアルポート名にマッチするか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Serial port not found.")
                        break
                    else:
                        Dict_Machine_Name_Num[Nc_Command] = int(Machine_Number) #####辞書にOコマンドと配列番号を登録
                        #DSerial[Nc_Command] = Nc_val #####辞書に登録
                        DICT_MACHINE_WORK_STAT[Nc_Command] = 0 #####辞書にOコマンドと実行結果を登録
                        DICT_MACHINE_FIN_STAT[Nc_Command] = 0 #####辞書にOコマンドと動作状況を登録
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole("SET :" +  Nc_Command + " is " + Nc_val + ".")
                        ret = OConnect(Nc_val, Dict_Machine_Name_Num[Nc_Command])
                        if(ret > 0):
                            break
                        else:
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole("CONNECTION : " + Nc_Command + " through " + Nc_val + " succeed.")
                            time.sleep(0.1)
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need = for SET command.")
                    break
            #####


        #####
        Current_Line_Number = Current_Line_Number + 1
        if(Current_Line_Number == Total_Line_Number):
            isError = 0 #ループ中にエラーが無かったとする
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                print("")
                print("[INSTRUMENT NAME AND COMMUNICATION NUMBER FOR LIST]")
                print(Dict_Machine_Name_Num)
                print("")
                print("[LINE NUMBER OF N COMMAND AGAINST P COMMAND]")
                print(Dict_Jump_Distination_Num)
                print("")
            WConsole(">CHECKING SETTINGS DONE!")
            WConsole("")
            break


    #####行の先頭へ移動
    win.ui.plainTextEdit_1.moveCursor(QtGui.QTextCursor.End) #####指定した行へ移動
    cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number)) #####指定した行へ移動
    win.ui.plainTextEdit_1.setTextCursor(cursor) #####指定した行へ移動
    win.ui.plainTextEdit_1.setFocus
    #####




















    ########################################################################################################
    ########################################################################################################
    ##############################プログラムの文法確認と、各行のプログラムの配列化##############################
    ########################################################################################################
    ########################################################################################################
    if(isError == 0):
        isError = 1
        Current_Line_Number = 0 #####現在の行番号
        Nc_Program = [] #####プログラム記憶用配列
        #Nc_Program_LINE =[] #####プログラムの各行記憶用配列
        WConsole(">CHECKING PROGRAM...")
        while(True):
            app.processEvents() #####ループ中もプロセスが動作する様にする
            #D_PROGRAM_LINE.clear()
            #PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
            
            #####指定行を取得
            PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
            win.ui.plainTextEdit_1.moveCursor(QtGui.QTextCursor.End) #####指定した行へ移動
            cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number)) #####指定した行へ移動
            win.ui.plainTextEdit_1.setTextCursor(cursor) #####指定した行へ移動
            cursor = win.ui.plainTextEdit_1.textCursor() #####選択範囲をハイライト表示する
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock, QtGui.QTextCursor.KeepAnchor, 1) #####選択範囲をハイライト表示する
            win.ui.plainTextEdit_1.setTextCursor(cursor) #####選択範囲をハイライト表示する
            win.ui.plainTextEdit_1.setFocus
            app.processEvents() #####ループ中もプロセスが動作する様にする
            time.sleep(float(win.ui.comboBox_2.currentText()))
            #####


            #========================================コマンド#用========================================
            if(PText.startswith("#") == True):
                if(":" in PText) == True: ##########分岐##########
                    vals = PText.split(":") #####:で分割
                    if ("=" in vals[0]) == False:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need =.")
                        break
                    val_01 = vals[0].split("=")
                    if DIGIT_CHK(val_01[0], ["#"], str(Current_Line_Number)) == False:break
                    if DIGIT_CHK(val_01[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                    if("=" in vals[1]) == True: #####分岐が演算の場合
                        val_23 = vals[1].split("=")
                        if DIGIT_CHK(val_23[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(val_23[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "="
                    elif ("+" in vals[1]) == True:
                        val_23 = vals[1].split("+")
                        if DIGIT_CHK(val_23[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(val_23[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "+"
                    elif ("-" in vals[1]) == True:
                        val_23 = vals[1].split("-")
                        if DIGIT_CHK(val_23[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(val_23[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "-"
                    elif ("P" in vals[1]) == True: #####分岐がジャンプの場合
                        if(vals[1] in Dict_Jump_Distination_Num) == False:
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : N number not found.")
                            break
                        val_23 = ["P", vals[1].replace("P", ""), str(Current_Line_Number)]
                        if DIGIT_CHK(val_23[1], []) == False:break
                        chr = "J"
                    else:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong format.")
                        break
                    if("#" in val_01[1]) == True and (val_01[1] in DICT_VARIABLE.keys())  == False:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                        break
                    if("#" in val_23[0]) == True and (val_23[0] in DICT_VARIABLE.keys())  == False:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                        break
                    if("#" in val_23[1]) == True and (val_23[1] in DICT_VARIABLE.keys())  == False:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                        break
                    line = [":", "=", val_01[0], val_01[1], chr, val_23[0], val_23[1]]
                    Nc_Program.append(line)
                    DICT_VARIABLE[val_01[0]] = ""
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole(str(val_01[0]) + " " + str(val_01[1]) + " " + str(val_23[0]) + " " + str(val_23[1]))
                else: ##########代入##########
                    if("=" in PText) == True:
                        vals= PText.split("=")
                        if DIGIT_CHK(vals[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(vals[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "="
                    elif("+" in PText) == True:
                        vals= PText.split("+")
                        if DIGIT_CHK(vals[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(vals[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "+"
                    elif("-" in PText) == True:
                        vals= PText.split("-")
                        if DIGIT_CHK(vals[0], ["#"], str(Current_Line_Number)) == False:break
                        if DIGIT_CHK(vals[1], ["#", "-", "."], str(Current_Line_Number)) == False:break
                        chr = "-"
                    else:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong format.")
                        break
                    if("#" in vals[1]) == True and (vals[1] in DICT_VARIABLE.keys())  == False:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                        break
                    line = [":", chr, vals[0], vals[1]]
                    Nc_Program.append(line)
                    DICT_VARIABLE[vals[0]] = ""
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole(str(vals[0]) + " " +  str(vals[1]))
            #####


            #========================================コマンドA用========================================
            elif(PText.startswith("A") == True):
                if((PText in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : XA not found.")
                    break
                else:
                    Nc_Program.append(["A", int(PText.replace("A", ""))]) #####Aと番号をリストに追加
            #####


            #========================================コマンドB用========================================
            elif(PText.startswith("B") == True):
                if((PText in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : RCP not found.")
                    break
                else:
                    Nc_Program.append(["B", int(PText.replace("B", ""))]) #####Aと番号をリストに追加
            #####


            #========================================コマンドC用========================================
            elif(PText.startswith("C") == True):
                Nc_Program.append(["C"])
            #####


            #========================================コマンドE用========================================
            elif(PText.startswith("E") == True):
                if ("S" in PText) == False:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need speed value.")
                    break
                if ("A" in PText) == False:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need acceleration value.")
                    break
                vals = PText.replace("E", "")
                vals = vals.replace("S", "")
                vals = vals.replace("A", "")
                vals = vals.split(" ")
                if len(vals) != 3:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need 3 values.")
                    break 
                ChkNum = vals[0].replace(".", "")
                ChkNum = ChkNum.replace("+", "")
                ChkNum = ChkNum.replace("-", "")
                ChkNum = ChkNum.replace("#", "")
                if(ChkNum.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                ChkNum = vals[1].replace(".", "")
                ChkNum = ChkNum.replace("+", "")
                ChkNum = ChkNum.replace("-", "")
                if(ChkNum.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                ChkNum = vals[2].replace(".", "")
                ChkNum = ChkNum.replace("+", "")
                ChkNum = ChkNum.replace("-", "")
                if(ChkNum.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                #####変数が辞書にあるか確認
                if(("#" in vals[0]) == True and (vals[0] in DICT_VARIABLE.keys())  == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                    break
                #####
                Nc_Program.append(["E", vals[0], vals[1], vals[2]]) #####Aと番号をリストに追加
            #####


            #========================================コマンドF用========================================
            elif(PText.startswith("F") == True):
                    Nc_Program.append(["F"]) #####Aと番号をリストに追加
            #####


            #========================================コマンドG用========================================
            elif(PText.startswith("G4 U") == True):
                Nc_Command = PText.replace("G4 U", "") #####Nc_Commandの文字列から"G4 U"を削除
                ChkNum = Nc_Command
                ChkNum = ChkNum.replace(".", "")
                if(ChkNum.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                Nc_Program.append(["G", "4", float(Nc_Command)]) #####Aと番号をリストに追加
            #####


            #========================================コマンドH用========================================
            elif(PText.startswith("H") == True):
                if(PText == "H0"):
                    Nc_Program.append(["H", "0"])
                elif(PText == "H1"):
                    Nc_Program.append(["H", "1"])
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : H commands must be H0 or H1.")
                    break   
            #####


            #========================================コマンドI用(測定)========================================
            elif(PText.startswith("I") == True and (" P" in PText) == True):
                Command, Value = PText.split(" ")
                if((Command in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Instrument not found.")
                    break
                elif((Value in Dict_Jump_Distination_Num) == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : N number not found.")
                    break
                else:
                    Nc_Program.append(["I", Command, "P", Value])
            #####


            #========================================コマンドI用(センサー用途　現在値記憶)========================================
            elif(PText.startswith("I") == True and (" R" in PText) == True):
                Command, Value = PText.split(" ")
                if((Command in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Instrument not found.")
                    break
                else:
                    Nc_Program.append(["I", Command, "R"])
            #####


            #========================================コマンドI用(センサー用途　記憶値と現在値を比較)========================================
            elif(PText.startswith("I") == True and (" C" in PText) == True):
                Command, Value = PText.split(" ")
                Value = Value.replace("C", "P")
                if((Command in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Instrument not found.")
                    break
                elif((Value in Dict_Jump_Distination_Num) == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : N number not found.")
                    break
                else:
                    Nc_Program.append(["I", Command, "C", Value])
            #####


            #========================================コマンドJ用========================================
            elif(PText.startswith("J") == True):
                Value = PText.replace("J", "")
                Value = Value.replace(".", "")
                if(Value.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                Value = float(PText.replace("J", ""))
                if(Value < 0.01 or Value > 3):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number must be from 0.01 to 3.")
                    break
                else:
                    Nc_Program.append(["J", Value])
            #####


            #========================================コマンドK用========================================
            elif(PText.startswith("K") == True):
                Value = PText.replace("K", "")
                if(Value.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                Value = int(Value)
                if(Value < 0 or Value > 63):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Number must be from 0 to 63.")
                    break
                else:
                    if(Value < 10): #####ポジション番号が一桁台の場合
                        Value_HEX = str(Value)
                        Value_HEX.replace("0x", "")
                        Value_HEX = "0" + Value_HEX
                    else:
                        Value_HEX = str(Value)
                        Value_HEX.replace("0x", "")
                    Nc_Program.append(["K", Value, Value_HEX])
            #####


            #========================================コマンドL用========================================
            elif(PText.startswith("L") == True):
                if((PText in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : PLC not found.")
                    break
                else:
                    Nc_Program.append(["L", int(PText.replace("L", ""))]) #####Lと番号をリストに追加
            #####


            #========================================コマンドM用========================================
            elif(PText.startswith("M200") == True): #####（ＲＳ－０１）待合せ（複数動作中の機器が完了するまでプログラムを停止する）            
                Nc_Program.append(["M", "200"])
            elif(PText.startswith("M99 P") == True):
                Command = PText.replace("M99 P", "") #####Nc_Commandの文字列から"M99 P"を削除
                if(Command.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                PText = PText.replace("M99 ", "")
                if((PText in Dict_Jump_Distination_Num) == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : N number not found.")
                    break
                Nc_Program.append(["M", "99", "P", PText])
            elif(PText.startswith("M99") == True):
                if len(PText.replace("M99", "")) == 0:
                    Nc_Program.append(["M", "99", ""])
                else:
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong command after M99.")
                    break
            elif(PText.startswith("M22") == True): #####エラーディテクトモードオフ（現在動作中の機器が動作完了するまでプログラムを停止する）
                Nc_Program.append(["M", "22"])
            elif(PText.startswith("M21") == True): #####エラーディテクトモードオン（機器の同時動作を可能にする）
                Nc_Program.append(["M", "21"])
            elif(PText.startswith("M20") == True): #####ワンサイクルストップ
                Nc_Program.append(["M", "20"])
            elif(PText.startswith("M4 T") == True):
                Value = PText.replace("M4 T", "") #####Nc_Commandの文字列から"M4 T"を削除
                Value = Value.replace(".", "") #####Nc_Commandの文字列から"."を削除
                if(Value.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                Value = PText.replace("M4 T", "") #####Nc_Commandの文字列から"M4 T"を削除
                Nc_Program.append(["M", "4", Value])
            #####


            #========================================Oコマンド用========================================
            elif(PText.startswith("O") == True):
                if((PText in Dict_Machine_Name_Num) != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : KM-1U not found.")
                    break
                else:
                    Nc_Program.append(["O", int(PText.replace("O", ""))]) #####Oと番号をリストに追加
            #####


            #========================================Pコマンド用========================================
            #PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
            elif(PText.startswith("P") == True):
                PText = PText.replace(" ", "")
                Nc_Command, Nc_Command2 = PText.split("S")
                Nc_Command = Nc_Command.replace("P", "") #####Nc_Commandの文字列から"P"を削除
                Nc_Command2, Nc_Command3 = Nc_Command2.split("C")
                #Nc_Command2 = Nc_Command2.replace("S", "") #####Nc_Commandの文字列から"S"を削除
                tmp = Nc_Command.replace("-", "")
                if(tmp.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                if(Nc_Command2.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                if(Nc_Command3 != "0" and Nc_Command3 != "1"):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Must be 0 or 1.")
                    break
                Nc_Program.append(["P", Nc_Command, Nc_Command2, Nc_Command3])
            #####

            #========================================コマンドQ用========================================
            elif(PText.startswith("Q") == True):
                Nc_Program.append(["Q"])
            #####


            #========================================コマンドR用========================================
            elif(PText.startswith("R") == True):
                if((" P" in PText) == True):
                    PText, Nc_val = PText.split(" P") #####PTextの文字列を" P"で分割し、PTextとNc_valに代入
                    if(Nc_val.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    else:
                        Pval = "P" + Nc_val
                        if((Pval in Dict_Jump_Distination_Num) == False):
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : N number not found.")
                            break
                        else:
                            Nc_val = Pval #####ジャンプ先P番号
                else:
                    Nc_val = "" #####ジャンプ先P番号なし

                #####特定ポート値取得用
                if(("=" in PText) == True):
                    PText, Lbit = PText.split("=") #####PTextの文字列を"="で分割し、PTextとLbitに代入
                    com = PText.replace("R", "")
                    if(Lbit.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    tmp = Lbit.replace("0", "")
                    tmp = tmp.replace("1", "")
                    LLen = len(tmp)
                    if(LLen > 0):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Format error.")
                        break
                    Nc_Program.append(["R", com, Lbit, Nc_val, "0"]) #####Rコマンド　ビットナンバー　値　ジャンプ先

                #####変動ポート値取得用
                elif(("," in PText) == True):
                    com = PText
                    com = com.replace("R", "")
                    com = com.replace(" ", "")
                    com = com.replace("*", "")
                    com = com.replace(",", "")
                    com = com.replace("#", "")
                    #DIGIT_CHK(com, ["R", " ", "*", ",", "#"], Current_Line_Number)
                    if(com.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Format error.")
                        break
                    com = PText
                    com = com.replace("R", "")
                    com = com.replace(" ", "")
                    com = com.split(",")
                    #####配列内の変数が登録されているか確認（特殊な例）
                    error_status = 0 
                    for x in com:
                        if(("#" in x) == True and (x in DICT_VARIABLE.keys())  == False):
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                            error_status = 1
                    if(error_status == 1):
                        break
                    #####
                    Nc_Program.append(["R", com, "", Nc_val, "1"]) #####Rコマンド　ビットナンバー　値　ジャンプ先

                #####全ポート値取得用
                else:
                    com = PText
                    com = com.replace("R", "")
                    com = com.replace(" ", "")
                    com = com.replace("0", "")
                    com = com.replace("1", "")
                    LLen = len(com)
                    if(LLen > 0):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Format error.")
                        break
                    com = PText.replace("R", "")
                    com = com.replace(" ", "")
                    Nc_Program.append(["R", com, "", Nc_val, "2"]) #####Rコマンド　ビット列　値無し　ジャンプ先
            #####


            #========================================コマンドT用========================================
            elif(PText.startswith("T") == True):
                Nc_Command = PText.replace("T", "") #####Nc_Commandの文字列から"T"を削除
                if(Nc_Command.isdigit() == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                    break
                Nc_Program.append(["T", Nc_Command])
            #####


            #========================================コマンドW用========================================
            elif(PText.startswith("W") == True):
                #####特定ポート値指定用
                if(("=" in PText) == True):
                    PText, Lbit = PText.split("=") #####PTextの文字列を"="で分割し、PTextとLbitに代入
                    com = PText.replace("W", "")
                    if(com.isdigit() == False):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need number.")
                        break
                    tmp = Lbit.replace("0", "")
                    tmp = tmp.replace("1", "")
                    LLen = len(tmp)
                    if(LLen > 0):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Format error.")
                        break
                    Nc_Program.append(["W", com, Lbit])
                else:
                    com = PText.replace("W", "")
                    com = com.replace(" ", "")
                    com = com.replace("0", "")
                    com = com.replace("1", "")
                    LLen = len(com)
                    if(LLen > 0):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Format error.")
                        break
                    com = PText.replace("W", "")
                    com = com.replace(" ", "")
                    Nc_Program.append(["W", com, ""])
            #####


            else:
                if(PText != "" and PText.startswith("N") != True and PText.startswith("SET ") != True and PText.startswith("(") != True):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Unknown command.")
                    break
                else:
                    Nc_Program.append([""])

            Current_Line_Number = Current_Line_Number + 1
            if(Current_Line_Number == Total_Line_Number):
                isError = 0
                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                    print("[TRANSLATED PROGRAM]")
                    print(Nc_Program)
                    print("")
                WConsole(">CHECKING PROGRAM DONE!")
                WConsole("")
                break


        #####行の先頭へ移動
        win.ui.plainTextEdit_1.moveCursor(QtGui.QTextCursor.End) #####指定した行へ移動
        cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number)) #####指定した行へ移動
        win.ui.plainTextEdit_1.setTextCursor(cursor) #####指定した行へ移動
        win.ui.plainTextEdit_1.setFocus
        #####




















    ######################################################################################
    ######################################################################################
    ##############################配列化されたプログラムの実行##############################
    ######################################################################################
    ######################################################################################
    if(isError == 0):
        Total_Line_Number = win.ui.plainTextEdit_1.blockCount() #####plainTextEdit_1の行数を取得

        #####仮想並列処理のN番号を取得
        #CNG1_4
        VirtualNum = len(VirtualValue)
        for i, l in enumerate(VirtualValue):
            if i > 0:
                if((l[0] in Dict_Jump_Distination_Num) == False):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : " + i[0] + " number not found.")
                    break
                VirtualValue[i][0] = Dict_Jump_Distination_Num[l[0]]
 
        while(True):

            #####現在の仮想並列処理のパラメータを取得
            Current_Line_Number = VirtualValue[VirtualCurrentNum][0]
            SelectedPLC = VirtualValue[VirtualCurrentNum][1]
            SelectedXA = VirtualValue[VirtualCurrentNum][2]
            SelectedRCP = VirtualValue[VirtualCurrentNum][3]
            SelectedKM = VirtualValue[VirtualCurrentNum][4]
            #CNG4_2
            ERROR_DETECT = VirtualValue[VirtualCurrentNum][5]
            #CNG4_2
            #CNG1_4

            #####指定行を取得
            #CNG2_3
            #PText = win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number).text() #####PTextにplainTextEdit_1の指定行を代入
            win.ui.plainTextEdit_1.moveCursor(QtGui.QTextCursor.End) #####指定した行へ移動
            if VirtualDisplay > -1:
                cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(VirtualValue[VirtualDisplay][0])) #####指定した行へ移動
            else:
                cursor = QtGui.QTextCursor(win.ui.plainTextEdit_1.document().findBlockByLineNumber(Current_Line_Number)) #####指定した行へ移動
                #CNG2_3
            win.ui.plainTextEdit_1.setTextCursor(cursor) #####指定した行へ移動
            cursor = win.ui.plainTextEdit_1.textCursor() #####選択範囲をハイライト表示する
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock, QtGui.QTextCursor.KeepAnchor, 1) #####選択範囲をハイライト表示する
            win.ui.plainTextEdit_1.setTextCursor(cursor) #####選択範囲をハイライト表示する
            win.ui.plainTextEdit_1.setFocus
            app.processEvents() #####ループ中もプロセスが動作する様にする
            time.sleep(float(win.ui.comboBox_2.currentText()))
            #####


            #========================================コマンド#用========================================
            if(Nc_Program[Current_Line_Number][0] ==":"):
                if len(Nc_Program[Current_Line_Number]) == 4:
                    Val_1 = Nc_Program[Current_Line_Number][1]
                    Val_2 = Nc_Program[Current_Line_Number][2]
                    Val_3 = Nc_Program[Current_Line_Number][3]
                    #if ("#" in Val_3) == True  and (Val_3 in DICT_VARIABLE) == False:
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                        #break
                    if Val_1 == "=":
                        if ("#" in Val_3) == True:
                            DICT_VARIABLE[Val_2] = DICT_VARIABLE[Val_3]
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "=" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                        else:
                            DICT_VARIABLE[Val_2] = float(Val_3)
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "=" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                    elif Val_1 == "+":
                        if ("#" in Val_3) == True:
                            DICT_VARIABLE[Val_2] += DICT_VARIABLE[Val_3]
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "+" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                        else:
                            DICT_VARIABLE[Val_2] += float(Val_3)
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "+" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                    elif Val_1 == "-":
                        if ("#" in Val_3) == True:
                            DICT_VARIABLE[Val_2] -= DICT_VARIABLE[Val_3]
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "-" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                        else:
                            DICT_VARIABLE[Val_2] -= float(Val_3)
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Val_2 + "-" + Val_3)
                                WConsole(str(DICT_VARIABLE[Val_2]))
                                WConsole("")
                    else:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong format.")
                        break
                elif len(Nc_Program[Current_Line_Number]) == 7:
                    Val_2 = Nc_Program[Current_Line_Number][2]
                    Val_3 = Nc_Program[Current_Line_Number][3]
                    Val_4 = Nc_Program[Current_Line_Number][4]
                    Val_5 = Nc_Program[Current_Line_Number][5]
                    Val_6 = Nc_Program[Current_Line_Number][6]
                    #if ("#" in Val_2) == True  and (Val_2 in DICT_VARIABLE) == False:
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                        #break
                    #if ("#" in Val_3) == True  and (Val_3 in DICT_VARIABLE) == False:
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                        #break
                    #if ("#" in Val_5) == True  and (Val_5 in DICT_VARIABLE) == False:
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                        #break
                    #if ("#" in Val_6) == True  and (Val_6 in DICT_VARIABLE) == False:
                        #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                        #break
                    flag = 0
                    if ("#" in Val_3):
                        if DICT_VARIABLE[Val_2] == DICT_VARIABLE[Val_3]:
                            flag = 1
                    else:
                        if DICT_VARIABLE[Val_2] == float(Val_3):
                            flag = 1
                    if flag == 1:
                        if Val_4 == "=":
                            if ("#" in Val_6):
                                DICT_VARIABLE[Val_5] = DICT_VARIABLE[Val_6]
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "=" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                            else:
                                DICT_VARIABLE[Val_5] = float(Val_6)
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "=" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                        elif Val_4 == "+":
                            if ("#" in Val_6):
                                DICT_VARIABLE[Val_5] += DICT_VARIABLE[Val_6]
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "+" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                            else:
                                DICT_VARIABLE[Val_5] += float(Val_6)
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "+" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                        elif Val_4 == "-":
                            if ("#" in Val_6):
                                DICT_VARIABLE[Val_5] -= DICT_VARIABLE[Val_6]
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "-" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                            else:
                                DICT_VARIABLE[Val_5] -= float(Val_6)
                                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                    WConsole(Val_5 + "-" + Val_6)
                                    WConsole(str(DICT_VARIABLE[Val_5]))
                                    WConsole("")
                        elif Val_4 == "J":
                            Current_Line_Number = Dict_Jump_Distination_Num[Val_5 + Val_6] - 1 #####Current_Line_Numberがカウントされる事を考慮
                        else:
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong format.")
                            break
            #####


            #========================================コマンドA用========================================
            elif(Nc_Program[Current_Line_Number][0] =="A"):
                SelectedXA = Nc_Program[Current_Line_Number][1]
            #####


            #========================================コマンドB用========================================
            elif(Nc_Program[Current_Line_Number][0] =="B"):
                SelectedRCP = Nc_Program[Current_Line_Number][1]
            #####


            #========================================コマンドC用========================================
            elif(Nc_Program[Current_Line_Number][0] =="C"):
                if(ERROR_DETECT == 0):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Only works when the mode is M21.")
                    break
                Current_RCP = SelectedRCP #####現在選択されているRCPを記憶（マルチスレッド時のタイミング用）
                if(Current_RCP == -1): #####RCPが選択されているか確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : RCP not selected.")
                    break
                work_ChkVal = DICT_MACHINE_WORK_STAT["B" + str(Current_RCP)] #####現在選択されているRCPの動作状況を代入
                if(work_ChkVal == 1): #####選択したRCP動作中か確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : The RCP is already in use.")
                    break
                else:
                    #####開始
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "050407FF00", Current_RCP) #アラームリセット（実行）
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "0504070000", Current_RCP) #アラームリセット（通常状態に戻す）
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "050403FF00", Current_RCP) #サーボオン
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "0504010000", Current_RCP) #セーフティー加速無効
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "05040B0000", Current_RCP) #原点復帰準備
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    ret, _ = COMM_RCP("0" + str(Current_RCP) + "05040BFF00", Current_RCP) #原点復帰
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    start_Time = time.time()
                    while(True):
                        ret, result = COMM_RCP("0" + str(Current_RCP) + "0390050001", Current_RCP) #原点復帰完了確認
                        if ret > 0:
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                            break
                        ret, result = RESPONSE_TO_BYTES(result)
                        if ret > 0:
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Error occured while converting from HEX to BYTES.")
                            break
                        if result[11] == "1":
                            break
                        elapsed_Time = time.time() - start_Time
                        if elapsed_Time > MOVE_TIME_OUT: #Check elapsed time of communication.
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                            break
                        time.sleep(0.01)
            #####


            #========================================コマンドE用========================================
            elif(Nc_Program[Current_Line_Number][0] =="E"):
                Current_RCP = SelectedRCP #####現在選択されているRCPを記憶（マルチスレッド時のタイミング用）
                if(Current_RCP == -1): #####RCPが選択されているか確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : RCP not selected.")
                    break
                work_ChkVal = DICT_MACHINE_WORK_STAT["B" + str(Current_RCP)] #####現在選択されているRCPの動作状況を代入
                if(work_ChkVal == 1): #####選択したRCP動作中か確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : The RCP is already in use.")
                    break
                else:
                    #####開始
                    THREAD_LOCK.acquire()
                    DICT_MACHINE_WORK_STAT["B" + str(Current_RCP)] = 1 #####RCPを使用中にする
                    THREAD_LOCK.release()

                    ret = 0
                    resistor = 7
                    r_ret, registor = DECIMAL_TO_HEX(resistor, 4)
                    ret = ret + r_ret
                    r_ret, bit_num = DECIMAL_TO_HEX(resistor * 2, 2)
                    ret = ret + r_ret
                    val = Nc_Program[Current_Line_Number][1]
                    if ("#" in val) == True:
                        if (val in DICT_VARIABLE) == False:
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to set the variable first.")
                            break
                        else:
                            position = float(DICT_VARIABLE[val]) #移動位置（変数）
                    else:
                        position = float(val) #移動位置（数値）
                    r_ret, position = DECIMAL_TO_HEX(int(position * 100), 8)
                    ret = ret + r_ret
                    range = RCP_POS_DIFF #移動誤差
                    r_ret, range = DECIMAL_TO_HEX(int(range * 100), 8)
                    ret = ret + r_ret
                    speed = float(Nc_Program[Current_Line_Number][2]) #移動速度
                    r_ret, speed = DECIMAL_TO_HEX(int(speed * 100), 8)
                    ret = ret + r_ret
                    acceleration_deceleration = float(Nc_Program[Current_Line_Number][3]) #加減速度
                    r_ret, acceleration_deceleration = DECIMAL_TO_HEX(int(acceleration_deceleration * 100), 4)
                    ret = ret + r_ret
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Error occured while converting data for RCP.")
                        break
                    e_com = "0" + str(Current_RCP) + "109900" + registor + bit_num + position + range + speed + acceleration_deceleration
                    ret, _ = COMM_RCP(e_com, Current_RCP) #移動命令送信
                    if ret > 0:
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                        break
                    if(ERROR_DETECT == 0):
                        #CNG3_3
                        VirtualMachine[VirtualCurrentNum].append("B" + str(Current_RCP)) #仮想並列処理で使用する機器を登録
                        #CNG3_3
                        Thread = threading.Thread(target = BMove ,args=(Current_RCP,))
                        Thread.start() #####完了処理はM200で行う
                    else:
                        ret = BMove(Current_RCP)
                        if(ret == 1):
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                            break
            #####


            #========================================コマンドF用========================================
            elif(Nc_Program[Current_Line_Number][0] =="F"):
                WConsole(">Program is stoped by F command.")
                break
            #####


            #========================================コマンドG用========================================
            elif(Nc_Program[Current_Line_Number][0] =="G"):
                if(Nc_Program[Current_Line_Number][1] =="4"):
                    time.sleep(Nc_Program[Current_Line_Number][2])
            #####


            #========================================コマンドH用========================================
            elif(Nc_Program[Current_Line_Number][0] == "H"):
                if(Nc_Program[Current_Line_Number][1] == "0"):
                    H_FAIL_VAL = H_FAIL_COUNTER
                elif(Nc_Program[Current_Line_Number][1] == "1"):
                    H_FAIL_VAL = H_FAIL_VAL - 1
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("Message : H value is " + str(H_FAIL_VAL) + ".")
                    if(H_FAIL_VAL <= 0):
                        WConsole("Message : H counter is up.")
                        break
            #####


            #========================================コマンドI用========================================
            elif(Nc_Program[Current_Line_Number][0] == "I"):
                if(ERROR_DETECT == 0):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Only works when the mode is M21.")
                    break
                #####コマンドI用(測定)
                elif(Nc_Program[Current_Line_Number][2] == "P"):
                    ret = IMeasure(Nc_Program[Current_Line_Number][1], Dict_Machine_Name_Num[Nc_Program[Current_Line_Number][1]])
                    if(ret == 1):
                        break
                    elif(ret == 2):
                        Current_Line_Number = Dict_Jump_Distination_Num[Nc_Program[Current_Line_Number][3]] - 1
                #####コマンドI用(センサー用途　現在値記憶)
                elif(Nc_Program[Current_Line_Number][2] == "R"):
                    ret = IRead(Nc_Program[Current_Line_Number][1], Dict_Machine_Name_Num[Nc_Program[Current_Line_Number][1]])
                    if(ret == 1):
                        break
                #####コマンドI用(センサー用途　記憶値と現在値を比較)
                elif(Nc_Program[Current_Line_Number][2] == "C"):
                    ret = ICheck(Nc_Program[Current_Line_Number][1], Dict_Machine_Name_Num[Nc_Program[Current_Line_Number][1]])
                    if(ret == 1):
                        break
                    elif(ret == 2):
                        Current_Line_Number = Dict_Jump_Distination_Num[Nc_Program[Current_Line_Number][3]] - 1
            #####


            #========================================コマンドJ用========================================
            elif(Nc_Program[Current_Line_Number][0] == "J"):
                RCP_POS_DIFF = Nc_Program[Current_Line_Number][1]
            #####


            #========================================コマンドK用========================================
            elif(Nc_Program[Current_Line_Number][0] == "K"):
                XApos = Nc_Program[Current_Line_Number][1]
                Current_Xa = SelectedXA #####現在選択されているXAを記憶（マルチスレッド時のタイミング用）
                if(Current_Xa == -1): #####PLCが選択されているか確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : XA not selected.")
                    break
                work_ChkVal = DICT_MACHINE_WORK_STAT["A" + str(Current_Xa)] #####現在選択されているXAの動作状況を代入
                if(work_ChkVal == 1): #####選択したXA動作中か確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : The XA is already in use.")
                    break
                else:
                    #####開始
                    THREAD_LOCK.acquire()
                    DICT_MACHINE_WORK_STAT["A" + str(Current_Xa)] = 1 #####XAを使用中にする
                    THREAD_LOCK.release()
                    XAstr = Nc_Program[Current_Line_Number][2] #####16BIT文字列を代入
                    LIST_XA[Current_Xa].write(bytes("0MP" + XAstr + "\r\n", "utf-8")) #指定したティーチングデータの位置に移動
                    Lbuf = ""
                    MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
                    while(True):
                        Bbuf = LIST_XA[Current_Xa].readline()
                        Lbuf = Lbuf + Bbuf.decode("utf-8")
                        if(("\n" in Lbuf) == True):
                            ret = 0
                            break
                        #####タイムアウト確認
                        ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                        if(ElapsedTime > MOVE_TIME_OUT):
                            WConsole("XA : " + Lbuf)
                            WConsole("ERROR : No response in time.")
                            THREAD_LOCK.acquire()
                            DICT_MACHINE_WORK_STAT["A" + str(Current_Xa)] = 0 #####XAを使用可能にする
                            THREAD_LOCK.release()
                            ret = 1
                            break
                        #####
                        app.processEvents() #####ループ中もプロセスが動作する様にする
                    #####

                    if(ret == 1): #####通信エラーが発生した場合
                        break
                    else: #####通信に成功した場合
                        if(ERROR_DETECT == 0):
                            #CNG3_4
                            VirtualMachine[VirtualCurrentNum].append("A" + str(Current_Xa)) #仮想並列処理で使用する機器を登録
                            #CNG3_4
                            Thread = threading.Thread(target = AMove ,args=(Current_Xa,))
                            Thread.start() #####完了処理はM200で行う
                        else:
                            ret = AMove(Current_Xa)
                            if(ret == 1):
                                WConsole("ERROR LINE " + str(Current_Line_Number) + " : Communication error.")
                                break
            #####


            #========================================コマンドL用========================================
            elif(Nc_Program[Current_Line_Number][0] =="L"):
                SelectedPLC = Nc_Program[Current_Line_Number][1]
            #####


            #========================================コマンドM用========================================
            elif(Nc_Program[Current_Line_Number][0] =="M"):
                if(Nc_Program[Current_Line_Number][1] =="200"):
                    
                    #CNG1_1
                    l = 0
                    #CNG3_7
                    #DKeys = DICT_MACHINE_WORK_STAT.keys()
                    DKeys = VirtualMachine[VirtualCurrentNum]
                    #CNG3_7
                    for i in DKeys:
                        l = l + DICT_MACHINE_WORK_STAT[i]
                    if(l > 0): #####全ての機器が動作完了しているか確認(動作している場合はlが0より大きくなる)
                        Current_Line_Number = Current_Line_Number -1 #動作が完了してない場合は再度M200の確認をする様にする
                        #CNG3_8
                        VirtualMachine[VirtualCurrentNum].clear()
                        #CNG3_8
                    #CNG1_1
                    l = 0
                    #CNG3_9
                    #DKeys = DICT_MACHINE_FIN_STAT.keys()
                    DKeys = VirtualMachine[VirtualCurrentNum]
                    #CNG3_9
                    for i in DKeys:
                        l = l + DICT_MACHINE_FIN_STAT[i]
                    if(l > 0): #####各機器でエラーが発生しているか確認(発生している場合はlが0より大きくなる)
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : M200 catched error.")
                        WConsole(">Value follwed by command must be 0 to work properly.")
                        WConsole(">Check the program or the machine to fix it.")
                        for i in DKeys:
                            WConsole(i +" : " + str(l))
                        break
                    
                    #time.sleep(0.2) #####マルチスレッド完了後のタイミング合わせ用（マルチスレッドの同時書込み問題で、時間が短いと次回Ｄｏｂｏｔの軸移動で失敗する）
                elif(Nc_Program[Current_Line_Number][1] =="99" and Nc_Program[Current_Line_Number][2] =="P"):
                    Current_Line_Number = Dict_Jump_Distination_Num[Nc_Program[Current_Line_Number][3]] - 1 #####Current_Line_Numberがカウントされる事を考慮
                elif(Nc_Program[Current_Line_Number][1] =="99" and Nc_Program[Current_Line_Number][2] ==""):
                    Current_Line_Number = - 1 #####Current_Line_Numberがカウントされる事を考慮
                elif(Nc_Program[Current_Line_Number][1] =="22"):
                    ERROR_DETECT = 0
                elif(Nc_Program[Current_Line_Number][1] =="21"):
                    ERROR_DETECT = 1
                elif(Nc_Program[Current_Line_Number][1] =="20"):
                    LOOP_COUNT = LOOP_COUNT + 1
                    win.ui.lineEdit_4.setText(str(LOOP_COUNT))
                    #WConsole("")
                    if(win.ui.checkBox_1.isChecked() == True):
                        win.ui.pushButton_1.setEnabled(True)
                        win.ui.pushButton_2.setEnabled(True)
                        win.ui.groupBox_1.setEnabled(False)
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole(">Program is paused.")
                        AOTO_MODE_STAT = 2
                elif(Nc_Program[Current_Line_Number][1] =="4"):
                    MOVE_TIME_OUT = str(Nc_Program[Current_Line_Number][2])
            #####


            #========================================コマンドO用========================================
            elif(Nc_Program[Current_Line_Number][0] =="O"):
                SelectedKM = Nc_Program[Current_Line_Number][1]
            #####

            #========================================コマンドP用========================================
            elif(Nc_Program[Current_Line_Number][0] =="P"):
                Current_Km = SelectedKM #####現在選択されているPLCを記憶（マルチスレッド時のタイミング用）
                if(Current_Km == -1): #####KM-1Uが選択されているか確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : KM-1U not selected.")
                    break
                LIST_KM[Current_Km].set_curve_type(int(Nc_Program[Current_Line_Number][3]))
                LIST_KM[Current_Km].set_speed(utils.rpm2rad_per_sec(int(Nc_Program[Current_Line_Number][2]))) #rpm-> rad/sec
                LIST_KM[Current_Km].move_by_dist(utils.deg2rad(int(Nc_Program[Current_Line_Number][1])),None) #Degree-> rad
            #####


            #========================================コマンドQ用========================================
            elif(Nc_Program[Current_Line_Number][0] =="Q"):
                WConsole("NG")
                NG_VAL = NG_VAL + 1
                win.ui.lineEdit_5.setText(str(NG_VAL))
            #####


            #========================================コマンドR用========================================
            elif(Nc_Program[Current_Line_Number][0] =="R"):

                if(Nc_Program[Current_Line_Number][3] != ""): #####ジャンプ先が指定されている場合
                    if(ERROR_DETECT == 0):
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : Only works when the mode is M21.")
                        break
                    Nc_val = Nc_Program[Current_Line_Number][3] #####ジャンプ先を記憶
                    Current_Plc = SelectedPLC #####現在選択されているPLCを記憶（マルチスレッド時のタイミング用）
                    if(Current_Plc == -1): #####PLCが選択されているか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : PLC not selected.")
                        break
                    else:
                        #####通信開始
                        LIST_PLC[Current_Plc].write(bytes("I", "utf-8")) #####PLCの入力ポート値を取得
                        #time.sleep(0.05)
                        Lbuf = ""
                        MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
                        while(True):
                            Bbuf = LIST_PLC[Current_Plc].readline()
                            Lbuf = Lbuf + Bbuf.decode("utf-8")
                            if(("E" in Lbuf) == True):
                                ret = 0
                                break
                            #####タイムアウト確認
                            ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                            if(ElapsedTime > MOVE_TIME_OUT):
                                WConsole("ERROR : No response in time.")
                                ret = 1
                                break
                            #####
                            app.processEvents() #####ループ中もプロセスが動作する様にする
                        #####
                        if(ret == 1): #####通信エラーが発生した場合
                            break
                        else: #####通信に成功した場合
                            Lbuf = Lbuf.replace("E", "")
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                WConsole(Lbuf)
                            Lbuf_Len = len(Lbuf)
                            Process_Pattern = Nc_Program[Current_Line_Number][4]
                            ####################「特定ビット参照」　"R"　ビット位置　ビット値　ジャンプ先　処理パターン　「例：R1=1 P5」####################
                            if(Process_Pattern == "0"):
                                if(Nc_Program[Current_Line_Number][1] == ""): #####ビット位置が取得ビット内にあるか確認
                                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need parameter postion.")
                                    break
                                Bpos = Nc_Program[Current_Line_Number][1] #####ビット位置
                                com = Nc_Program[Current_Line_Number][2] #####ビット値
                                LLen = int(Bpos) + 1 #####ビット位置迄のビット長
                                if(Lbuf_Len < LLen): #####ビット位置が取得ビット内にあるか確認
                                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Wrong bit position.")
                                    break
                                else:
                                    Lbuf_list = list(Lbuf)
                                    InputBit = Lbuf_list[int(Bpos)] 
                                    if InputBit == com:
                                        Current_Line_Number = Dict_Jump_Distination_Num[Nc_val] - 1 #####ジャンプ　Current_Line_Numberがカウントされる事を考慮
                            ####################「変動ビット参照」　"R"　ビット配列　値無し　ジャンプ先　処理パターン　「例：R0,*,#1,0 ,0,0,0,0 P5」####################
                            elif(Process_Pattern == "1"):
                                Lbuf_list = list(Lbuf)
                                com = ""
                                for i, x in enumerate(Nc_Program[Current_Line_Number][1]):
                                    if(("#" in x) == True):
                                        #if((x in DICT_VARIABLE.keys())  == False):
                                            #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                                            #break
                                        x = str(int(DICT_VARIABLE[x]))
                                    if(x == "0"):
                                        com += "0"
                                    elif(x == "1"):
                                        com += "1"
                                    elif(x == "*"):
                                        com += Lbuf_list[i]
                                LLen = len(com) #####指定した命令長を記憶
                                if(LLen != Lbuf_Len): #####命令パラメータ長が合うか確認
                                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Parameter length mismatch.")
                                    break
                                else:
                                    if(Lbuf == com): #####入力ポートの状態が指定した状態と同じか確認
                                        Current_Line_Number = Dict_Jump_Distination_Num[Nc_val] - 1 #####ジャンプ　Current_Line_Numberがカウントされる事を考慮
                            ####################「総ビット参照」　"R"　ビット値　値無し　ジャンプ先　処理パターン　「例：R0000 0001 P5」####################
                            else:
                                com = Nc_Program[Current_Line_Number][1] #####総ビット値
                                LLen = len(com) #####指定した命令長を記憶
                                if(LLen != Lbuf_Len): #####命令パラメータ長が合うか確認
                                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Parameter length mismatch.")
                                    break
                                else:
                                    if(Lbuf == com): #####入力ポートの状態が指定した状態と同じか確認
                                        Current_Line_Number = Dict_Jump_Distination_Num[Nc_val] - 1 #####ジャンプ　Current_Line_Numberがカウントされる事を考慮

                else:  #####ジャンプ先が指定されていない場合
                    Current_Plc = SelectedPLC #####現在選択されているPLCを記憶（マルチスレッド時のタイミング用）
                    if(Current_Plc == -1): #####PLCが選択されているか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : PLC not selected.")
                        break
                    work_ChkVal = DICT_MACHINE_WORK_STAT["L" + str(Current_Plc)] #####現在選択されているPLCの動作状況を代入
                    if(work_ChkVal == 1): #####選択したPLC動作中か確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : The PLC is already in use.")
                        break
                    else:
                        #####開始
                        THREAD_LOCK.acquire()
                        DICT_MACHINE_WORK_STAT["L" + str(Current_Plc)] = 1 #####PLCを使用中にする
                        THREAD_LOCK.release()
                        Process_Pattern = Nc_Program[Current_Line_Number][4]
                        ####################「特定ビット参照」　"R"　ビット位置　ビット値　値無し　処理パターン　「例：R1=1」####################
                        if(Process_Pattern == "0"):
                            Mode = 0
                        ####################「変動ビット参照」　"R"　ビット配列　値無し　値無し　処理パターン　「例：R0,*,#1,0 ,0,0,0,0」####################
                        elif(Process_Pattern == "1"):
                            Mode = 1
                        ####################「総ビット参照」　"R"　ビット値　値無し　値無し　処理パターン　「例：R0000 0001」####################
                        else:
                            Mode = 2
                        if(ERROR_DETECT == 0):
                            #CNG3_5
                            VirtualMachine[VirtualCurrentNum].append("L" + str(Current_Plc)) #仮想並列処理で使用する機器を登録
                            #CNG3_5
                            Thread = threading.Thread(target = LCheck ,args=(Nc_Program[Current_Line_Number], Current_Plc, Mode,))
                            Thread.start() #####完了処理はM200で行う
                        else:
                            ret = LCheck(Nc_Program[Current_Line_Number], Current_Plc, Mode)
                            if(ret > 0):
                                break
            #####


            #========================================コマンドT用========================================
            elif(Nc_Program[Current_Line_Number][0] =="T"):
                if(Nc_Program[Current_Line_Number][1] == "0"):
                    Timer = 0
                else:
                    Timer = 1
                    TimeOut = int(Nc_Program[Current_Line_Number][1])
                    MoveStartTime = time.time()
            #####


            #========================================コマンドW用========================================
            elif(Nc_Program[Current_Line_Number][0] =="W"):
                if(ERROR_DETECT == 0):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Only works when the mode is M21.")
                    break
                #####特定ポート値指定用
                if(Nc_Program[Current_Line_Number][2] != ""):
                    Lbit = Nc_Program[Current_Line_Number][2]
                    Bpos = Nc_Program[Current_Line_Number][1]
                    LLen = int(Bpos) + 1 #####指定した命令長を記憶
                    Current_Plc = SelectedPLC #####現在選択されているPLCを記憶（マルチスレッド時のタイミング用）
                    if(Current_Plc == -1): #####PLCが選択されているか確認
                        WConsole("ERROR LINE " + str(Current_Line_Number) + " : PLC not selected.")
                        break
                    else:
                        #####開始
                        LIST_PLC[Current_Plc].write(bytes("O", "utf-8")) #####命令パラメータ長を確認
                        #time.sleep(0.05)
                        Lbuf = ""
                        MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
                        while(True):
                            Bbuf = LIST_PLC[Current_Plc].readline()
                            Lbuf = Lbuf + Bbuf.decode("utf-8")
                            if(("E" in Lbuf) == True): #####送信終了文字を確認
                                ret = 0
                                break
                            #####タイムアウト確認
                            ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                            if(ElapsedTime > MOVE_TIME_OUT):
                                WConsole("ERROR : No response in time.")
                                ret = 1
                                break
                            #####
                            app.processEvents() #####ループ中もプロセスが動作する様にする
                        #####
                        if(ret == 1): #####通信エラーが発生した場合
                            break               
                        else: #####通信に成功した場合
                            Lbuf = Lbuf.replace("E", "") #####受信したデータから終了記号を削除
                            if(LLen > len(Lbuf)): #####命令パラメータ長が合うか確認
                                WConsole("ERROR LINE " + str(Current_Line_Number) + " : Parameter position mismatch.")
                                break
                        Lbuf_list = list(Lbuf)
                        Lbuf_list[int(Bpos)] = Lbit
                        com = "".join(Lbuf_list)
                else:
                    com = Nc_Program[Current_Line_Number][1]
                #####
                LLen = len(com) #####指定した命令長を記憶
                Current_Plc = SelectedPLC #####現在選択されているPLCを記憶（マルチスレッド時のタイミング用）
                if(Current_Plc == -1): #####PLCが選択されているか確認
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : PLC not selected.")
                    break
                else:
                    #####開始
                    LIST_PLC[Current_Plc].write(bytes("O", "utf-8")) #####命令パラメータ長を確認
                    #time.sleep(0.05)
                    Lbuf = ""
                    MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
                    while(True):
                        Bbuf = LIST_PLC[Current_Plc].readline()
                        Lbuf = Lbuf + Bbuf.decode("utf-8")
                        if(("E" in Lbuf) == True): #####送信終了文字を確認
                            ret = 0
                            break
                        #####タイムアウト確認
                        ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                        if(ElapsedTime > MOVE_TIME_OUT):
                            WConsole("ERROR : No response in time.")
                            ret = 1
                            break
                        #####
                        app.processEvents() #####ループ中もプロセスが動作する様にする
                    #####
                    if(ret == 1): #####通信エラーが発生した場合
                        break
                    else: #####通信に成功した場合
                        Lbuf = Lbuf.replace("E", "") #####受信したデータから終了記号を削除
                        if(LLen != len(Lbuf)): #####命令パラメータ長が合うか確認
                            WConsole("ERROR LINE " + str(Current_Line_Number) + " : Parameter length mismatch.")
                            break
                        else: #####命令パラメータ長が合った場合
                            LIST_PLC[Current_Plc].write(bytes(com, "utf-8")) #####命令パラメータを送信し実行
                            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                                time.sleep(0.2)          
                                #####開始
                                LIST_PLC[Current_Plc].write(bytes("O", "utf-8")) #####命令パラメータ実行後の状態を確認
                                Lbuf = ""
                                MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
                                while(True):
                                    Bbuf = LIST_PLC[Current_Plc].readline()
                                    Lbuf = Lbuf + Bbuf.decode("utf-8")
                                    if(("E" in Lbuf) == True):
                                        Lbuf = Lbuf.replace("E", "")
                                        ret = 0
                                        break
                                    #####タイムアウト確認
                                    ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                                    if(ElapsedTime > MOVE_TIME_OUT):
                                        WConsole("ERROR : No response in time.")
                                        ret = 1
                                        break
                                    #####
                                    app.processEvents() #####ループ中もプロセスが動作する様にする
                                #####
                                if(ret == 1): #####通信エラーが発生した場合
                                    break
                                else: #####通信に成功した場合
                                    WConsole(Lbuf)
            #####

             #####タイマーがオンの場合の処理
            if(Timer == 1):
                ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
                if(ElapsedTime > TimeOut):
                    WConsole("ERROR LINE " + str(Current_Line_Number) + " : Timeout.")
                    break

            Current_Line_Number = Current_Line_Number + 1
            if(Current_Line_Number == Total_Line_Number): #####最終行まで来たら実行終了
                WConsole(">Program ended.")
                break

            #####次の仮想並列処理に移行
            #CNG1_5
            VirtualValue[VirtualCurrentNum][0] = Current_Line_Number
            VirtualValue[VirtualCurrentNum][1] = SelectedPLC
            VirtualValue[VirtualCurrentNum][2] = SelectedXA
            VirtualValue[VirtualCurrentNum][3] = SelectedRCP
            VirtualValue[VirtualCurrentNum][4] = SelectedKM
            #CNG4_3
            VirtualValue[VirtualCurrentNum][5] = ERROR_DETECT
            #CNG4_3
            VirtualCurrentNum += 1
            if VirtualCurrentNum == VirtualNum:
                VirtualCurrentNum = 0
            #CNG1_5
            
            if(AOTO_MODE_STAT == 2): #####シングルブロックがオンの場合ループする
                win.ui.pushButton_1.setEnabled(True)
                win.ui.pushButton_2.setEnabled(True)
                win.ui.groupBox_1.setEnabled(False)
                if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                    WConsole(">Program is paused.")
                while(True):
                    if(AOTO_MODE_STAT != 2):
                        break
                    app.processEvents() #####ループ中もプロセスが動作する様にする
            if(AOTO_MODE_STAT == 0): #####ストップが押された場合は実行終了
                break
            if(win.ui.checkBox_2.isChecked() == True):
                AOTO_MODE_STAT = 2





    #####マルチスレッド動作が完了しているか確認(終了する前にシリアル通信を切断すると再接続出来なくなる)
    MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
    while(True):
        l = 0
        DKeys = DICT_MACHINE_WORK_STAT.keys()
        for i in DKeys:
            l = l + DICT_MACHINE_WORK_STAT[i]
        if(l == 0): #####全ての機器が動作完了しているか確認(動作している場合はlが0より大きくなる)
            break
        #####タイムアウト確認
        ElapsedTime = time.time() - MoveStartTime #####移動タイムアウト確認用（経過時間）
        if(ElapsedTime > MOVE_TIME_OUT):
            WConsole("ERROR : No response in time.")
            WConsole("ERROR : May need to restart computer to reconnect.")
            break
        #####
        app.processEvents() #####ループ中もプロセスが動作する様にする
    #####


    try:
        for i in DKeys:
            if(i.startswith("I") == True):
                LIST_INSTRUMENT[Dict_Machine_Name_Num[i]].close()
    except:
        WConsole("WRNING : Error disconnecting from measure instrument.")
    try:
        for i in DKeys:
            if(i.startswith("L") == True):
                LIST_PLC[Dict_Machine_Name_Num[i]].close()
        #####
    except:
        WConsole("WRNING : Error disconnecting from PLC.")
    try:
        for i in DKeys:
            if(i.startswith("A") == True):
                LIST_XA[Dict_Machine_Name_Num[i]].close()
        #####
    except:
        WConsole("WRNING : Error disconnecting from XA.")
    try:
        for i in DKeys:
            if(i.startswith("B") == True):
                LIST_RCP[Dict_Machine_Name_Num[i]].close()
        #####
    except:
        WConsole("WRNING : Error disconnecting from RCP.")

    try:
        for i in DKeys:
            if(i.startswith("O") == True):
                LIST_KM[Dict_Machine_Name_Num[i]].disable_action()
                LIST_KM[Dict_Machine_Name_Num[i]].disconnect()
                del LIST_KM[Dict_Machine_Name_Num[i]]
                #LIST_KM[Dict_Machine_Name_Num[i]].finish_auto_serial_reading()
        #####
    except:
        WConsole("WRNING : Error disconnecting from KM-1U.")
    win.ui.pushButton_1.setEnabled(True)
    win.ui.pushButton_2.setEnabled(False)
    win.ui.groupBox_1.setEnabled(True)
    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
        WConsole(">Program is stopped")
    AOTO_MODE_STAT = 0




















######################################################################################
######################################################################################
#######################################各種関数#######################################
######################################################################################
######################################################################################
#####文字列が数値か確認する関数
def DIGIT_CHK(STRING = "-100.0", EXCLUDE_LIST = ["+", "-", "."], LINE_NUM = "1"): #文字列　除外文字　行番号
    for x in EXCLUDE_LIST:
        STRING = STRING.replace(x, "")
    if STRING.isdigit() == True:
        return True
    else:
        WConsole("ERROR LINE " + LINE_NUM + " : Value must be in proper number format.")
        WConsole("ERROR : Charactors below are allowed in this case beside digits.")
        for x in EXCLUDE_LIST:
            WConsole("ERROR : " + x)
        return False
#####


#####コンソール表示用関数
def WConsole(cmd):
    cursor = win.ui.plainTextEdit_2.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.insertText(cmd + "\r\n")
    win.ui.plainTextEdit_2.setTextCursor(cursor)
#####


#####シリアルポート確認用関数
def Check_Serial():
    Serial_Number = []
    serial_list = serial.tools.list_ports.comports()
    if(len(serial_list) > 0):
        for i in range(len(serial_list)):
            Serial_Number.insert(i, str(serial_list[i].device))
    return(Serial_Number)
#####




















######################################################################################
######################################################################################
#####################################測定器用関数######################################
######################################################################################
######################################################################################
#####測定機器通信開始用関数
def IConnect(Nc_Command, Nc_val):
    global LIST_INSTRUMENT
    Nc_val_List = []
    Nc_val_List = DICT_INSTRUMENT_PARAM[Nc_Command].split(",")
    try:
        LIST_INSTRUMENT[Nc_val] = serial.Serial(
            port = Nc_val_List[0], 
            baudrate = int(Nc_val_List[1]), 
            bytesize = int(Nc_val_List[2]), 
            parity = Nc_val_List[3], 
            stopbits = int(Nc_val_List[4]), 
            timeout = 0.2, 
            xonxoff = 0, 
            rtscts = 0, 
            writeTimeout = 0.2, 
            dsrdtr = None)
        ret = 0
    except:
        ret = 1
        WConsole("ERROR : Measure insrument connection error.")
    return ret
#####


#####測定機測定値取得用関数
def IMeasure(Nc_Command, Nc_val):
    global LIST_INSTRUMENT
    global NG_VAL
    Nc_val_List = []
    Nc_val_List = DICT_INSTRUMENT_PARAM[Nc_Command].split(",")
    sPos = Nc_val_List[6]
    ePos = Nc_val_List[7]
    maxValue = Nc_val_List[8]
    minValue = Nc_val_List[9]

    try:
        i = 0
        while(True): #####何らかの原因で通信エラーが発生したら、再度通信を試みるようにする
            LIST_INSTRUMENT[Nc_val].write(bytes(Nc_val_List[5] + "\r", "utf-8")) #####測定値送信コマンドを測定器に送信
            time.sleep(0.1)
            ILine = LIST_INSTRUMENT[Nc_val].readline() #####測定値を取得
            l = len(ILine) - 1 #####測定値のバイト長を取得
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data length]")
                WConsole(str(l))
            IByte = ILine[0:l] #####バイト長のデータを取得
            IStr = IByte.decode("utf-8") #####バイトデータを文字列へ変換
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data]")
                WConsole(IStr)
            if(int(ePos) <= l):
                IByte = ILine[int(sPos):int(ePos)]
                IStr = IByte.decode()
                tmpIStr = IStr.replace("+" ,"")
                tmpIStr = tmpIStr.replace("-" ,"")
                tmpIStr = tmpIStr.replace("." ,"")
                if(tmpIStr.isdigit() == False):
                    WConsole("ERROR : Unexpected charactor included.")
                    WConsole("ERROR : Check communication setting.")
                    WConsole("ERROR : Maybe getting error message from instrument.")
                    WConsole("TRY : Get data again.")
                    ret = 1
                else:
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Position data]")
                        WConsole(IStr)
                    IFlo = float(IStr)
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Final data]")
                        WConsole(str(IFlo))
                    if(IFlo < float(maxValue) and IFlo >= float(minValue)):
                        WConsole(str(IFlo) + " OK")
                        ret =0
                        break
                    else:
                        WConsole(str(IFlo) + " NG")
                        NG_VAL = NG_VAL + 1
                        win.ui.lineEdit_5.setText(str(NG_VAL))
                        ret = 2
                        break
            else:
                WConsole("ERROR : Data length is shorter than expected.")
                WConsole("ERROR : Check communication setting.")
                WConsole("ERROR : Maybe getting error message from instrument.")
                WConsole("TRY : Get data again.")
                ret = 1
            i = i +1
            if(i == 5):
                WConsole("ERROR : Tried to communicate 5 times.")
                WConsole("ERROR : Check communication setting.")
                ret = 1
                break
            time.sleep(0.1)
            app.processEvents() #####ループ中もプロセスが動作する様にする
    except:
        WConsole("ERROR : Something is wrong with the communication or settings.")

    return ret
#####


#####測定機現在値記憶用関数
def IRead(Nc_Command, Nc_val):
    global LIST_INSTRUMENT
    global INSTRUMENT_CURRENT_VAL
    Nc_val_List = []
    Nc_val_List = DICT_INSTRUMENT_PARAM[Nc_Command].split(",")
    sPos = Nc_val_List[6]
    ePos = Nc_val_List[7]
    maxValue = Nc_val_List[8]
    minValue = Nc_val_List[9]

    try:
        i = 0
        while(True): #####何らかの原因で通信エラーが発生したら、再度通信を試みるようにする
            LIST_INSTRUMENT[Nc_val].write(bytes(Nc_val_List[5] + "\r", "utf-8")) #####測定値送信コマンドを測定器に送信
            time.sleep(0.1)
            ILine = LIST_INSTRUMENT[Nc_val].readline() #####測定値を取得
            l = len(ILine) - 1 #####測定値のバイト長を取得
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data length]")
                WConsole(str(l))
            IByte = ILine[0:l] #####バイト長のデータを取得
            IStr = IByte.decode("utf-8") #####バイトデータを文字列へ変換
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data]")
                WConsole(IStr)
            if(int(ePos) <= l):
                IByte = ILine[int(sPos):int(ePos)]
                IStr = IByte.decode()
                tmpIStr = IStr.replace("+" ,"")
                tmpIStr = tmpIStr.replace("-" ,"")
                tmpIStr = tmpIStr.replace("." ,"")
                if(tmpIStr.isdigit() == False):
                    WConsole("ERROR : Unexpected charactor included.")
                    WConsole("ERROR : Check communication setting.")
                    WConsole("ERROR : Maybe getting error message from instrument.")
                    WConsole("TRY : Get data again.")
                    ret = 1
                else:
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Position data]")
                        WConsole(IStr)
                    IFlo = float(IStr)
                    INSTRUMENT_CURRENT_VAL = IFlo
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Final data]")
                        WConsole(str(IFlo))
                    ret = 0
                    break
            else:
                WConsole("ERROR : Data length is shorter than expected.")
                WConsole("ERROR : Check communication setting.")
                WConsole("ERROR : Maybe getting error message from instrument.")
                WConsole("TRY : Get data again.")
                ret = 1
            i = i +1
            if(i == 5):
                WConsole("ERROR : Tried to communicate 5 times.")
                WConsole("ERROR : Check communication setting.")
                ret = 1
                break
            time.sleep(0.1)
            app.processEvents() #####ループ中もプロセスが動作する様にする
    except:
        WConsole("ERROR : Something is wrong with the communication or settings.")

    return ret
#####


#####測定機記憶値比較用関数
def ICheck(Nc_Command, Nc_val):
    global LIST_INSTRUMENT
    Nc_val_List = []
    Nc_val_List = DICT_INSTRUMENT_PARAM[Nc_Command].split(",")
    sPos = Nc_val_List[6]
    ePos = Nc_val_List[7]
    maxValue = Nc_val_List[8]
    minValue = Nc_val_List[9]

    try:
        i = 0
        while(True): #####何らかの原因で通信エラーが発生したら、再度通信を試みるようにする
            LIST_INSTRUMENT[Nc_val].write(bytes(Nc_val_List[5] + "\r", "utf-8")) #####測定値送信コマンドを測定器に送信
            time.sleep(0.1)
            ILine = LIST_INSTRUMENT[Nc_val].readline() #####測定値を取得
            l = len(ILine) - 1 #####測定値のバイト長を取得
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data length]")
                WConsole(str(l))
            IByte = ILine[0:l] #####バイト長のデータを取得
            IStr = IByte.decode("utf-8") #####バイトデータを文字列へ変換
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole("[Raw data]")
                WConsole(IStr)
            if(int(ePos) <= l):
                IByte = ILine[int(sPos):int(ePos)]
                IStr = IByte.decode()
                tmpIStr = IStr.replace("+" ,"")
                tmpIStr = tmpIStr.replace("-" ,"")
                tmpIStr = tmpIStr.replace("." ,"")
                if(tmpIStr.isdigit() == False):
                    WConsole("ERROR : Unexpected charactor included.")
                    WConsole("ERROR : Check communication setting.")
                    WConsole("ERROR : Maybe getting error message from instrument.")
                    WConsole("TRY : Get data again.")
                    ret = 1
                else:
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Position data]")
                        WConsole(IStr)
                    IFlo = float(IStr)
                    if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                        WConsole("[Final data]")
                        WConsole(str(IFlo))
                    if(IFlo >= INSTRUMENT_CURRENT_VAL - 0.1 and IFlo <= INSTRUMENT_CURRENT_VAL + 0.1):
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole(str(IFlo) + " Value not changed.")
                        ret =0
                        break
                    else:
                        if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                            WConsole(str(IFlo) + " Value changed.")
                        ret = 2
                        break
            else:
                WConsole("ERROR : Data length is shorter than expected.")
                WConsole("ERROR : Check communication setting.")
                WConsole("ERROR : Maybe getting error message from instrument.")
                WConsole("TRY : Get data again.")
                ret = 1
            i = i +1
            if(i == 5):
                WConsole("ERROR : Tried to communicate 5 times.")
                WConsole("ERROR : Check communication setting.")
                ret = 1
                break
            time.sleep(0.1)
            app.processEvents() #####ループ中もプロセスが動作する様にする
    except:
        WConsole("ERROR : Something is wrong with the communication or settings.")

    return ret
#####




















######################################################################################
######################################################################################
######################################PLC用関数#######################################
######################################################################################
######################################################################################
#####PLC通信開始用関数
def LConnect(PLC_Comport, Nc_val):
    global LIST_PLC
    try:
        LIST_PLC[Nc_val] = serial.Serial(port=PLC_Comport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.2, xonxoff=0, rtscts=0, dsrdtr=None)
        ret = 0
    except:
        ret = 1
        WConsole("ERROR : PLC connection error.")
    return ret
#####


#####入力ポート確認用関数（ジャンプ無し、エラーディテクトオフ対応）
def LCheck(Nc_Program, Current_Plc, Mode):

    global DICT_MACHINE_WORK_STAT
    global DICT_MACHINE_FIN_STAT

    MoveStartTime = time.time() #####タイムアウト確認用（開始時間）
    while(True):


        #####通信開始
        LIST_PLC[Current_Plc].write(bytes("I", "utf-8")) #####PLCの入力ポート値を取得
        #time.sleep(0.05)
        Lbuf = ""
        MoveStartTime2 = time.time() #####タイムアウト確認用（開始時間）
        while(True):
            Bbuf = LIST_PLC[Current_Plc].readline()
            Lbuf = Lbuf + Bbuf.decode("utf-8")
            if(("E" in Lbuf) == True):
                ret = 0
                break
            #####タイムアウト確認
            ElapsedTime2 = time.time() - MoveStartTime2 #####タイムアウト確認用（経過時間）
            if(ElapsedTime2 > MOVE_TIME_OUT):
                ret = 1
                break
            #####
            app.processEvents() #####ループ中もプロセスが動作する様にする
        #####

        if(ret == 0): #####通信が成功した場合
            Lbuf = Lbuf.replace("E", "")
            Lbuf_Len = len(Lbuf)
            ####################「特定ビット参照」　"R"　ビット位置　ビット値　「例：R1=1」####################
            if(Mode == 0):
                if(Nc_Program[1] == ""): #####ビット位置が取得ビット内にあるか確認
                    break
                Bpos = Nc_Program[1] #####ビット位置
                com = Nc_Program[2] #####ビット値
                LLen = int(Bpos) + 1 #####ビット位置迄のビット長
                if(Lbuf_Len < LLen): #####ビット位置が取得ビット内にあるか確認
                    ret = 1
                else:
                    Lbuf_list = list(Lbuf)
                    InputBit = Lbuf_list[int(Bpos)] 
                    if(InputBit == com):
                        ret = 0
                    else:
                        ret = 2
            ####################「変動ビット参照」　"R"　ビット配列　値無し　「例：R0,*,#1,0 ,0,0,0,0 P5」####################
            elif(Mode == 1):
                Lbuf_list = list(Lbuf)
                com = ""
                for i, x in enumerate(Nc_Program[1]):
                    if(("#" in x) == True):
                        #if((x in DICT_VARIABLE.keys())  == False):
                            #WConsole("ERROR LINE " + str(Current_Line_Number) + " : Need to define the variable first.")
                            #break
                        x = str(int(DICT_VARIABLE[x]))
                    if(x == "0"):
                        com += "0"
                    elif(x == "1"):
                        com += "1"
                    elif(x == "*"):
                        com += Lbuf_list[i] 
                LLen = len(com) #####指定した命令長を記憶
                if(LLen != Lbuf_Len): #####命令パラメータ長が合うか確認
                    ret = 1
                else:
                    if(Lbuf == com): #####入力ポートの状態が指定した状態と同じか確認
                        ret = 0
                    else:
                        ret = 2
            ####################総ビット参照　"R"　ビット値　値無し　「例：R0000 0001」####################
            else:
                com = Nc_Program[1] #####総ビット値
                LLen = len(com) #####指定した命令長を記憶
                if(LLen != Lbuf_Len): #####命令パラメータ長が合うか確認
                    ret = 1
                else:
                    if(Lbuf == com): #####入力ポートの状態が指定した状態と同じか確認
                        ret = 0
                    else:
                        ret = 2


        #####タイムアウト確認
        if(ret == 0 or ret == 1): #####通信、ビット符号確認でエラーが出てないか確認
            #if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                #WConsole(Lbuf)
            break
        ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
        if(ElapsedTime > MOVE_TIME_OUT):
            
            ret = 1
            break
        app.processEvents() #####ループ中もプロセスが動作する様にする
        #####

    THREAD_LOCK.acquire()
    DICT_MACHINE_WORK_STAT["L" + str(Current_Plc)] = 0 #####PLCを使用可能にする
    DICT_MACHINE_FIN_STAT["L" + str(Current_Plc)] = ret #####動作完了状況を記録（マルチスレッドモード用）
    THREAD_LOCK.release()
    return(ret)
    #####




















######################################################################################
######################################################################################
#######################################XA用関数#######################################
######################################################################################
######################################################################################
#####XA通信開始用関数
def AConnect(XA_Comport, Nc_val):
    global LIST_XA
    try:
        LIST_XA[Nc_val] = serial.Serial(port=XA_Comport, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.2, xonxoff=0, rtscts=0, dsrdtr=None)
        ret = 0
    except:
        ret = 1
        WConsole("ERROR : XA connection error.")
    return ret
#####


#####XA移動用関数（移動完了チェック有）
def AMove(Thread_Name_Num):

    global DICT_MACHINE_WORK_STAT
    global DICT_MACHINE_FIN_STAT

    #####移動完了確認
    Lbuf = ""
    LIST_XA[Thread_Name_Num].write(bytes("0RA\r\n", "utf-8")) #移動完了確認コマンド送信
    MoveStartTime = time.time() #####XA移動タイムアウト確認用（開始時間）
    while(True):
        Bbuf= LIST_XA[Thread_Name_Num].readline()
        Lbuf = Lbuf + Bbuf.decode("utf-8")
        if(("\n" in Lbuf) == True):
            if("1" in Lbuf):
                ret = 0
                break
            else:
                Lbuf = ""
                LIST_XA[Thread_Name_Num].write(bytes("0RA\r\n", "utf-8")) #移動完了確認コマンド送信
        #####タイムアウト確認
        ElapsedTime = time.time() - MoveStartTime #####タイムアウト確認用（経過時間）
        if(ElapsedTime > MOVE_TIME_OUT):
            ret = 1
            break
        #####
        app.processEvents() #####ループ中もプロセスが動作する様にする
        #####

    THREAD_LOCK.acquire()
    DICT_MACHINE_WORK_STAT["A" + str(Thread_Name_Num)] = 0 #####XAを使用可能にする
    DICT_MACHINE_FIN_STAT["A" + str(Thread_Name_Num)] = ret #####動作完了状況を記録（マルチスレッドモード用）
    THREAD_LOCK.release()
    return(ret)
#####




















######################################################################################
######################################################################################
#####################################RCP用種関数######################################
######################################################################################
######################################################################################
#####RCP通信開始用関数
def BConnect(RCP_Comport, Nc_val):
    global LIST_RCP
    try:
        LIST_RCP[Nc_val] = serial.Serial(port=RCP_Comport, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=0.2, xonxoff=0, rtscts=0, dsrdtr=None)
        ret = 0
    except:
        ret = 1
        WConsole("ERROR : RCP connection error.")
    return ret
#####


#####RCP通信用関数
def COMM_RCP(command, Nc_val):

    r_ret, LRC_Command = LRC_CREATE(command) #Process data to send.
    ret = 0
    ret += r_ret
    LIST_RCP[Nc_val].write(bytes(LRC_Command, 'utf-8'))
    start_Time = time.time()
    LRC_Command = ""
    while(True):
        serial_Buffer =LIST_RCP[Nc_val].readline()
        LRC_Command = LRC_Command + serial_Buffer.decode("utf-8")
        if ("\n" in LRC_Command) == True: #Check the charactors means the end of communication.
            r_ret, command = LRC_CHECK(LRC_Command) #Process received data.
            ret += r_ret
            return ret, command
        elapsed_Time = time.time() - start_Time
        if elapsed_Time > MOVE_TIME_OUT: #Check elapsed time of communication.
            ret += 1
            return ret
        app.processEvents() #####ループ中もプロセスが動作する様にする
#####


#####RCP移動用関数
def BMove(Thread_Name_Num):
    global DICT_MACHINE_WORK_STAT
    global DICT_MACHINE_FIN_STAT
    ret = 0
    start_Time = time.time()
    while(True):
        r_ret, result = COMM_RCP("0" + str(Thread_Name_Num) + "0390050001", Thread_Name_Num) #原点復帰完了確認
        ret = ret + r_ret
        if ret > 0:
            break
        r_ret, result = RESPONSE_TO_BYTES(result)
        ret = ret + r_ret
        if r_ret > 0:
            break
        if result[12] == "1":
            ret = 0
            break
        elapsed_Time = time.time() - start_Time
        if elapsed_Time > MOVE_TIME_OUT: #Check elapsed time of communication.
            ret = ret + 1
            break
        time.sleep(0.01)
        app.processEvents() #####ループ中もプロセスが動作する様にする
        #####

    THREAD_LOCK.acquire()
    DICT_MACHINE_WORK_STAT["B" + str(Thread_Name_Num)] = 0 #####RCPを使用可能にする
    DICT_MACHINE_FIN_STAT["B" + str(Thread_Name_Num)] = ret #####動作完了状況を記録（マルチスレッドモード用）
    THREAD_LOCK.release()
    return(ret)




















######################################################################################
######################################################################################
#####################################KM-1U用種関数######################################
######################################################################################
######################################################################################
#####KM-1U通信開始用関数
def OConnect(KM_Comport, Nc_val):
    global LIST_KM
    try:
        LIST_KM[Nc_val] = usbcontroller.USBController(KM_Comport, False)#, 115200, False)
        #LIST_KM[Nc_val].start_auto_serial_reading()
        #LIST_KM[Nc_val].connect()
        LIST_KM[Nc_val].enable_action()
        ret = 0
    except:
        ret = 1
        WConsole("ERROR : KM-1U connection error.")
    return ret
#####




















######################################################################################
######################################################################################
###################################PySide2用種関数####################################
######################################################################################
######################################################################################
#####Pysideのウィンドウ処理クラス########################################
class MainWindow1(QtWidgets.QMainWindow, Ui_MainWindow):
#=====GUI用クラス継承の定型文========================================
    def __init__(self, parent = None):
        super(MainWindow1, self).__init__(parent) 
        self.ui = Ui_MainWindow() #OCV3GUI内のクラスの読込
        self.ui.setupUi(self)
        self.ui.comboBox_2.addItems(["0", "0.1", "0.5", "1"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox_2.setCurrentIndex(0) #####コンボボックスのアイテムを選択
        #WConsole(self.ui.comboBox_2.currentText()) #####コンボボックスで選択されているアイテムをコピー
        #-----シグナルにメッソドを関連付け----------------------------------------
        self.ui.checkBox_3.clicked.connect(self.checkBox1_clicked) #checkBox1_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_1, QtCore.SIGNAL("clicked()"), self.pushButton1_clicked) #####pushButton1_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.pushButton2_clicked) #####pushButton2_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.pushButton3_clicked) #####pushButton3_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.pushButton4_clicked) #####pushButton4_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.pushButton5_clicked) #####pushButton5_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_6, QtCore.SIGNAL("clicked()"), self.pushButton6_clicked) #####pushButton6_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_7, QtCore.SIGNAL("clicked()"), self.pushButton7_clicked) #####pushButton7_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_8, QtCore.SIGNAL("clicked()"), self.pushButton8_clicked) #####pushButton8_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_9, QtCore.SIGNAL("clicked()"), self.pushButton9_clicked) #####pushButton9_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_10, QtCore.SIGNAL("clicked()"), self.pushButton10_clicked) #####pushButton10_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_11, QtCore.SIGNAL("clicked()"), self.pushButton11_clicked) #####pushButton11_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_12, QtCore.SIGNAL("clicked()"), self.pushButton12_clicked) #####pushButton12_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_13, QtCore.SIGNAL("clicked()"), self.pushButton13_clicked) #####pushButton13_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_14, QtCore.SIGNAL("clicked()"), self.pushButton14_clicked) #####pushButton14_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_15, QtCore.SIGNAL("clicked()"), self.pushButton15_clicked) #####pushButton15_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_16, QtCore.SIGNAL("clicked()"), self.pushButton16_clicked) #####pushButton16_clickedは任意
        QtCore.QObject.connect(self.ui.pushButton_17, QtCore.SIGNAL("clicked()"), self.pushButton17_clicked) #####pushButton17_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_1, QtCore.SIGNAL("clicked()"), self.radioButton1_checked) #####radioButton1_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_2, QtCore.SIGNAL("clicked()"), self.radioButton2_checked) #####radioButton2_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_3, QtCore.SIGNAL("clicked()"), self.radioButton3_checked) #####radioButton3_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_4, QtCore.SIGNAL("clicked()"), self.radioButton4_checked) #####radioButton4_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_5, QtCore.SIGNAL("clicked()"), self.radioButton5_checked) #####radioButton5_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_6, QtCore.SIGNAL("clicked()"), self.radioButton6_checked) #####radioButton6_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_7, QtCore.SIGNAL("clicked()"), self.radioButton7_checked) #####radioButton7_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_8, QtCore.SIGNAL("clicked()"), self.radioButton8_checked) #####radioButton8_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_9, QtCore.SIGNAL("clicked()"), self.radioButton9_checked) #####radioButton9_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_10, QtCore.SIGNAL("clicked()"), self.radioButton10_checked) #####radioButton10_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_11, QtCore.SIGNAL("clicked()"), self.radioButton11_checked) #####radioButton11_clickedは任意
        QtCore.QObject.connect(self.ui.radioButton_12, QtCore.SIGNAL("clicked()"), self.radioButton12_checked) #####radioButton12_clickedは任意
        #QtCore.QObject.connect(self.ui.checkBox_1, QtCore.SIGNAL("clicked()"), self.checkBox1_checked) #####checkBox1_clickedは任意
        #-----ウィジットのイベントをメインウィンドウで取得する設定----------------------------------------
        #self.ui.label1.installEventFilter(self)


#=====ウィジットのシグナル処理用メッソド========================================
    #-----checkBox1用イベント処理----------------------------------------
    def checkBox1_clicked(self):
        global Debug_Mode
        if(self.ui.checkBox_3.isChecked() == True):
            Debug_Mode = 1
        else:
            Debug_Mode = 0


    #-----pushButton1用イベント処理----------------------------------------
    def pushButton1_clicked(self):
        global AOTO_MODE_STAT
        if(AOTO_MODE_STAT == 0):
            self.ui.pushButton_1.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.groupBox_1.setEnabled(False)
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole(">Program is running.")
            if self.ui.checkBox_2.isChecked() == False:
                AOTO_MODE_STAT = 1
            else:
                AOTO_MODE_STAT = 2
            RUN_RS()
        elif(AOTO_MODE_STAT == 2):
            self.ui.pushButton_1.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.groupBox_1.setEnabled(False)
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole(">Program is restarted.")
            AOTO_MODE_STAT = 1


    #-----pushButton2用イベント処理----------------------------------------
    def pushButton2_clicked(self):
        global AOTO_MODE_STAT
        if(AOTO_MODE_STAT == 1):
            self.ui.pushButton_1.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.groupBox_1.setEnabled(False)
            if(Debug_Mode == 1): #<<<<<<<<<<<<<<<<<<<<デバッグモードの場合>>>>>>>>>>>>>>>>>>>>
                WConsole(">Program is paused.")
            AOTO_MODE_STAT = 2
        elif(AOTO_MODE_STAT == 2):
            self.ui.pushButton_1.setEnabled(True)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.groupBox_1.setEnabled(True)
            #WConsole(">Program is stopped.")
            AOTO_MODE_STAT = 0

    #-----pushButton3用イベント処理----------------------------------------
    def pushButton3_clicked(self):
        self.ui.groupBox_3.setEnabled(False)
        self.ui.groupBox_4.setEnabled(False)
        self.ui.groupBox_5.setEnabled(False)
        self.ui.pushButton_14.setEnabled(False)
        #dType.SetHOMECmd(api[self.ui.comboBox_1.currentIndex()],0) #####原点復帰
        time.sleep(25)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)
        self.ui.pushButton_6.setEnabled(True)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)
        self.ui.pushButton_9.setEnabled(True)
        self.ui.pushButton_10.setEnabled(True)
        self.ui.pushButton_11.setEnabled(True)
        self.ui.pushButton_14.setEnabled(True)
        self.ui.groupBox_3.setEnabled(True)
        self.ui.groupBox_4.setEnabled(True)
        self.ui.groupBox_5.setEnabled(True)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton4用イベント処理----------------------------------------
    def pushButton4_clicked(self):
        #pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0] + OVERRIDE_VAL, pose[1], pose[2], RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton5用イベント処理----------------------------------------
    def pushButton5_clicked(self):
        #pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0] - OVERRIDE_VAL, pose[1], pose[2], RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton6用イベント処理----------------------------------------
    def pushButton6_clicked(self):
        #pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0], pose[1] + OVERRIDE_VAL, pose[2], RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton7用イベント処理----------------------------------------
    def pushButton7_clicked(self):
        #pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0], pose[1] - OVERRIDE_VAL, pose[2], RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton8用イベント処理----------------------------------------
    def pushButton8_clicked(self):
        pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0], pose[1], pose[2] + OVERRIDE_VAL, RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton9用イベント処理----------------------------------------
    def pushButton9_clicked(self):
        #pose = dType.GetPose(api[self.ui.comboBox_1.currentIndex()]) #####ポジション取得
        DMove(1, pose[0], pose[1], pose[2] - OVERRIDE_VAL, RAPPID_VAL, self.ui.comboBox_1.currentIndex())
        time.sleep(0.2)
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton10用イベント処理----------------------------------------
    def pushButton10_clicked(self):
        cursor = self.ui.plainTextEdit_1.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        x, y, z = DPos(self.ui.comboBox_1.currentIndex())
        cursor.insertText("G1 " + "X" + x + " Y" + y + " Z" + z + " F100\r\n")
        self.ui.plainTextEdit_1.setTextCursor(cursor)

    #-----pushButton11用イベント処理----------------------------------------
    def pushButton11_clicked(self):
        DPos(self.ui.comboBox_1.currentIndex())

    #-----pushButton12用イベント処理----------------------------------------
    def pushButton12_clicked(self):
        serial_list = serial.tools.list_ports.comports()
        if(len(serial_list) > 0):
            for i in range(len(serial_list)):
                dev = str(serial_list[i].device)
                WConsole(dev)
        else:
            WConsole("ERROR : No serial port found.")

    #-----pushButton13用イベント処理----------------------------------------
    def pushButton13_clicked(self):
        if(self.ui.comboBox_1.currentIndex() != -1): #####コンボボックスのインデックスを確認
            ret = DConnect(self.ui.comboBox_1.currentText(), self.ui.comboBox_1.currentIndex()) #####Ｄｏｂｏｔに接続
            if(ret == 0):
                DPos(self.ui.comboBox_1.currentIndex())
                self.ui.pushButton_12.setEnabled(False)
                self.ui.pushButton_13.setEnabled(False)
                self.ui.pushButton_14.setEnabled(True)
                self.ui.groupBox_1.setEnabled(False)
                self.ui.groupBox_3.setEnabled(True)
                self.ui.groupBox_4.setEnabled(True)
                self.ui.groupBox_5.setEnabled(True)
                self.ui.comboBox_1.setEnabled(False)
                time.sleep(0.1)
        else:
            WConsole("ERROR : No serial port selected.")

    #-----pushButton14用イベント処理----------------------------------------
    def pushButton14_clicked(self):
        DDisconnect(self.ui.comboBox_1.currentIndex())
        self.ui.pushButton_12.setEnabled(True)
        self.ui.pushButton_13.setEnabled(True)
        self.ui.pushButton_14.setEnabled(False)
        self.ui.groupBox_1.setEnabled(True)
        self.ui.groupBox_3.setEnabled(False)
        self.ui.groupBox_4.setEnabled(False)
        self.ui.groupBox_5.setEnabled(False)
        self.ui.comboBox_1.setEnabled(True)
        time.sleep(0.2)

    #-----pushButton15用イベント処理----------------------------------------
    def pushButton15_clicked(self):
    #####ファイル読込
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'txt File (*.txt)')
        if filepath:
            #####ファイル名のみの取得
            filename1 = filepath.rsplit(".", 1) #ファイルパスの文字列右側から指定文字列で分割
            filename2 = filename1[0].rsplit("/", 1) #ファイルパスの文字列右側から指定文字列で分割
            os.chdir(filename2[0] + "/") #カレントディレクトリをファイルパスへ変更
            f = open(filename2[1] + "." + filename1[1], "r")
            text = f.read()
            f.close()
            self.ui.plainTextEdit_1.setPlainText(text)   
            #####
    #####

    #-----pushButton16用イベント処理----------------------------------------
    def pushButton16_clicked(self):
    #####ファイル書込み
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Open File", "",'txt File (*.txt)')
        if filepath:
            #####ファイル名のみの取得
            filename1 = filepath.rsplit(".", 1) #ファイルパスの文字列右側から指定文字列で分割
            filename2 = filename1[0].rsplit("/", 1) #ファイルパスの文字列右側から指定文字列で分割
            os.chdir(filename2[0] + "/") #カレントディレクトリをファイルパスへ変更
            f = open(filename2[1] + "." + filename1[1], "w")
            f.write(self.ui.plainTextEdit_1.toPlainText())
            f.close()
            msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
            msgbox.setText("FILE : Saved.") #####メッセージボックスのテキストを設定
            ret = msgbox.exec() #####メッセージボックスを表示
            #####
    #####
    #-----pushButton17用イベント処理----------------------------------------
    def pushButton17_clicked(self):
        global LOOP_COUNT
        global NG_VAL
        LOOP_COUNT = 0
        NG_VAL = 0
        self.ui.lineEdit_4.setText(str(LOOP_COUNT))
        self.ui.lineEdit_5.setText(str(NG_VAL))
    #####
    def radioButton1_checked(self):
        self.ui.pushButton_1.setEnabled(False)
        self.ui.pushButton_15.setEnabled(True)
        self.ui.pushButton_16.setEnabled(True)
        self.ui.pushButton_17.setEnabled(True)
        self.ui.plainTextEdit_1.setReadOnly(False)
        self.ui.groupBox_2.setEnabled(False)
        self.ui.groupBox_5.setEnabled(False)
        self.ui.groupBox_6.setEnabled(False)
        self.ui.groupBox_7.setEnabled(True)


    def radioButton2_checked(self):
        self.ui.pushButton_1.setEnabled(True)
        self.ui.pushButton_17.setEnabled(False)
        self.ui.plainTextEdit_1.setReadOnly(True)
        self.ui.groupBox_2.setEnabled(True)
        self.ui.groupBox_5.setEnabled(False)
        self.ui.groupBox_6.setEnabled(False)
        self.ui.groupBox_7.setEnabled(False)
        self.ui.comboBox_2.setEnabled(True)

    def radioButton3_checked(self):
        self.ui.pushButton_1.setEnabled(False)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)
        self.ui.pushButton_6.setEnabled(True)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)
        self.ui.pushButton_9.setEnabled(True)
        self.ui.pushButton_10.setEnabled(True)
        self.ui.pushButton_11.setEnabled(True)
        self.ui.pushButton_12.setEnabled(True)
        self.ui.pushButton_13.setEnabled(True)
        self.ui.pushButton_17.setEnabled(False)
        self.ui.plainTextEdit_1.setEnabled(True)
        self.ui.groupBox_2.setEnabled(False)
        self.ui.groupBox_6.setEnabled(True)
        self.ui.groupBox_7.setEnabled(False)
        self.ui.comboBox_1.setEnabled(True)
        self.ui.comboBox_1.clear() #####コンボボックスから全てのアイテムを削除
        Serial_Number = []
        Serial_Number = Check_Serial()
        self.ui.comboBox_1.addItems(Serial_Number) #####コンボボックスにアイテムを追加
        self.ui.comboBox_1.setCurrentIndex(-1) #####コンボボックスのアイテムを選択
        #WConsole(self.ui.comboBox_1.currentText()) #####コンボボックスで選択されているアイテムをコピー


    #def checkBox1_checked(self):


    def radioButton4_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 0.1

    def radioButton5_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 1

    def radioButton6_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 5

    def radioButton7_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 10

    def radioButton8_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 20

    def radioButton9_checked(self):
        global OVERRIDE_VAL
        OVERRIDE_VAL = 30

    def radioButton10_checked(self):
        global RAPPID_VAL
        RAPPID_VAL = 25

    def radioButton11_checked(self):
        global RAPPID_VAL
        RAPPID_VAL = 50

    def radioButton12_checked(self):
        global RAPPID_VAL
        RAPPID_VAL = 100




















######################################################################################
######################################################################################
#####################################メイン処理#######################################
######################################################################################
######################################################################################
#####メイン処理（グローバル）########################################
#=====メイン処理定型文========================================
if __name__ == '__main__':
    #app = QtGui.QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow1()
    win.show() #win.showFullScreen() win.showEvent()
    sys.exit(app.exec())
