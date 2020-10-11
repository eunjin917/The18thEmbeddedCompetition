#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include "Time.h"

#define BT_TX 2  // HM-10의 TX에 연결
#define BT_RX 3  // HM-10의 RX에 연결
#define vendor_code "341513" // vendor code
#define device_name "Dolphin" // device name
#define macaddress "3415131E31FD" // 필터링 할 자신의 slave 블루투스 맥주소

SoftwareSerial HM10(BT_TX,BT_RX);

String flag="0\n";

File myFile;

void setup(){
  Serial.begin(9600); // 전송속도 설정
  HM10.begin(9600);
  Wire.begin(8); // I2C통신을 하기위한 address(8)
  Wire.onReceive(receiveData); // 데이터를 받았을때 receiveDate함수를 실행
  /*--------------------------
  -> DS1302 시간 설정할 때 사용
  time_setting(__TIME__,__DATE__);
  --------------------------*/
  DS1302_Start(); // 시계모듈 실행

  if (!SD.begin(4)) { // SD카드 모듈을 초기화
    Serial.println("initialization failed!"); // SD카드 모듈 초기화에 실패하면 에러를 출력
    while (1);
  }
  // data.txt 열기
  myFile=SD.open("data.txt", FILE_WRITE);
  if (myFile){
    if(myFile.size()<=0){ // 데이터가 없을때 초기화 작업
      myFile.println(macaddress);
      myFile.close();
    }
  }
}

void loop(){
  HM10.write("AT+DISC?"); // Inquiry to HM10
  if (HM10.find((char*)"OK+DISC")){
    String Inquiry_Response=HM10.readString();
    String str=String_cleanup(Inquiry_Response);
    Serial.print(str); // 출력용
    // SD카드에 데이터 저장
    myFile = SD.open("data.txt", FILE_WRITE);
    if (myFile){ // 파일이 정상적으로 열리면 파일에 문자를 작성(추가)
      myFile.print(str);
      myFile.close(); // 파일을 닫기
    }
  }
}

String String_cleanup(String str){ // Inquiry 데이터 정리
  str=str.substring(2);
  
  String newStr="";
  String newTime=now(); // 현재시간
  
  for(int i=0;i<10;i++){
    str.replace("OK+DIS"+String(i)+":","");
  }
  str.replace("OK+NAME:"," ");
  
  //한줄씩 받아서 필터처리
  while(str!=""){
    String temp=str.substring(0,str.indexOf('\n'));
    if(temp.substring(0,6)==vendor_code && temp.substring(13,20)==device_name){
      if(!temp.startsWith(macaddress)){ // 자기 자신의 mac address도 필터하는 과정
        newStr+=temp.substring(0,13)+'\t'+newTime+'\t'+flag;
      }
    }
    str=str.substring(str.indexOf('\n')+1);
  }
  flag="0\n";
  return newStr;
}

void receiveData(int size) {
  while(Wire.available()>0) { // 데이터가 있으면 충돌발생을 의미
    Wire.read();
    flag="1\n";
  }
}
