#include <SoftwareSerial.h>
#define BT_RX 2  // HM-10의 TX에 연결
#define BT_TX 3  // HM-10의 RX에 연결

SoftwareSerial HM10(BT_RX,BT_TX);
 
void setup(){
  Serial.begin(9600); // 전송속도 설정
  HM10.begin(9600);
}
 
void loop(){
  if (HM10.available()) {
    Serial.write(HM10.read());
  }
  if (Serial.available()) {
    HM10.write(Serial.read());
  }
}