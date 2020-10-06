#include <SoftwareSerial.h>

#define BT_RX 2  // HM-10의 TX에 연결
#define BT_TX 3  // HM-10의 RX에 연결

SoftwareSerial HM10(BT_RX,BT_TX);

void setup() {
  Serial.begin(9600); // 전송속도 설정
  HM10.begin(9600);

  // 공장 초기화
  HM10.write("AT+RENEW"); 
  delay(1000);
  
  // HM-10 리붓
  HM10.write("AT+RESET");
  delay(1000);
  
  // iBeacon의 Major number설정 (0x1234는 임의값 설정 가능)
  HM10.write("AT+AT+MARJ0x1234");
  delay(1000);
  
  // iBeacon의 Minor number설정 (0xFA02는 임의값 설정 가능)
  HM10.write("AT+MINO0xFA02");
  delay(1000);
  
  // advertising(신호 송출) 주기를 5로 설정(약 0.5초)
  HM10.write("AT+ADVI5");//number 표기
  delay(1000);
  
  // HM-10 이름 정의 ( Dolphin[number] )
  HM10.write("AT+NAMEDolphin");
  delay(1000);
  
  // 전원 절약을 위해 맺지않음(non-connectable)모드로 설정
  HM10.write("AT+ADTY3");
  delay(1000);
  
  // iBeacon을 활성화
  HM10.write("AT+IBEA1");
  delay(1000);
  
  // iBeacon의 broadcast-only 로 설정
  HM10.write("AT+DELO2");
  delay(1000);
  
  // 전원 절약을 위해 auto-sleep으로 설정(최소 절전 모드)
  HM10.write("AT+PWRM0");
  delay(1000);
  
  // 리붓하여 반영
  HM10.write("AT+RESET");
  delay(1000);
}

void loop() {
  Serial.println("Set up successfully");
  delay(100);
}
