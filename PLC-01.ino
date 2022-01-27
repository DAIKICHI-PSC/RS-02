////////////////////ＳＲ－０１　Ｖ1.０////////////////////
//FOR FA-DUINO-24RA










////////////////////ライブラリ読込////////////////////

////////////////////変数と定義の設定////////////////////
/////GPIO関連
int in[100]; //入力ポート
int inStart = 30; //入力ポートの開始番号
int inNumber = 16; //入力ポートの数
int out[100]; //出力ポート
int outStart = 22; //出力ポートの開始番号
int outNumber = 8; //出力ポートの数

int i; //for用
int l; //for用

/////通信関連
byte ReadCHR = 0; //シリアル通信の文字列受信用変数
int pos = 1; //出力ポートの現在値
int iVal = 0; //入出力ポート値読み取り用










////////////////////電源投入時処理////////////////////
void setup()
{
  /////GPIOの設定
  l = inStart;
  for(i = 1; i<= inNumber; i++){
    in[i] = l;
    pinMode(in[i], INPUT);
    l++;
  }

  l = outStart;
  for(i = 1; i<= outNumber; i++){
    out[i] = l;
    pinMode(out[i], OUTPUT);
    l++;
  }

  /////通信関連
  Serial2.begin(115200);

}










////////////////////メイン処理////////////////////
void loop()
{
      //RS232C経由で命令を取得
      if(Serial2.available()){
        ReadCHR = Serial2.read();
        switch(ReadCHR){
          case 73: //I
            for(i = 1; i <= inNumber; i++){
              iVal = digitalRead(in[i]);
              if(iVal == 0){
                Serial2.write("0");
              }
              else{
                Serial2.write("1");
              }
            }
            Serial2.write("E");           
            break;
            
          case 79: //O
            for(i = 1; i <= outNumber; i++){
              iVal = digitalRead(out[i]);
              if(iVal == 0){
                Serial2.write("0");
              }
              else{
                Serial2.write("1");
              }
            }
            Serial2.write("E"); 
            break;

          case 48: //0
            digitalWrite(out[pos], LOW);
            pos = pos + 1;
            if(pos > outNumber){
              Serial2.write("E");
              pos = 1;
            }
            break;
            
          case 49: //1
            digitalWrite(out[pos], HIGH);
            pos = pos + 1;
            if(pos > outNumber){
              Serial2.write("E");
              pos = 1;
            }
            break;        
        }
      }

}
