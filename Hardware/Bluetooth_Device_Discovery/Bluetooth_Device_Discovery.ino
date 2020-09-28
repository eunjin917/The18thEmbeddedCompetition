#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include "Time.h"

#define BT_TX 2  // HM-10의 TX에 연결
#define BT_RX 3  // HM-10의 RX에 연결
#define vendor_code "341513" // vendor code
#define device_name "Dolphin" // device name

SoftwareSerial HM10(BT_TX,BT_RX);

String flag="0\n";

File myFile;

void setup(){
  Serial.begin(9600); // 전송속도 설정
  HM10.begin(9600);
  Wire.begin(8);
  Wire.onReceive(receiveData); //데이터를 받았을때 receiveDate함수를 실행
  /*--------------------------
  -> DS1302 시간 설정할떄만 사용
  time_setting(__TIME__,__DATE__);
  --------------------------*/
  DS1302_Start();

  if (!SD.begin(4)) { // SD카드 모듈을 초기화합니다.
    Serial.println("initialization failed!"); // SD카드 모듈 초기화에 실패하면 에러를 출력합니다.
    while (1);
  }
  myFile = SD.open("test.txt", FILE_WRITE);
}

void loop(){
  HM10.write("AT+DISC?"); // Inquiry to HM10
  if (HM10.find((char*)"OK+DIS")){
    String Inquiry_Response=HM10.readString();
    String str=String_cleanup(Inquiry_Response);
    //Serial.print(str);//출력용
    /*SD카드에 데이터 저장*/
    myFile = SD.open("test.txt", FILE_WRITE);
    if (myFile) { // 파일이 정상적으로 열리면 파일에 문자를 작성(추가)합니다.
      myFile.print(str);
      myFile.close(); // 파일을 닫습니다.
    }
  /*sd카드에 저장된 데이터 읽기
    myFile = SD.open("test.txt");
    if(myFile){
      while(myFile.available()){
        Serial.write(myFile.read());
      }
    }
    myFile.close();
  }
  */
}

String String_cleanup(String str){ //쿼리문 정리
  str=str.substring(2);
  
  String newStr="";
  String newTime=now();//현재시간
  
  for(int i=0;i<10;i++){
    str.replace("OK+DIS"+String(i)+":","");
  }
  str.replace("OK+NAME:"," ");
  
  //한줄씩 받아서 필터처리
  while(str!=""){
    String temp=str.substring(0,str.indexOf('\n'));
    if(temp.substring(0,6)==vendor_code && temp.substring(13,20)==device_name){
      newStr+=temp.substring(0,13)+"\t"+newTime+"\t"+flag;
    }
    str=str.substring(str.indexOf('\n')+1);
  }
  flag="0\n";
  return newStr;
}

void receiveData(int size) {
  while(Wire.available()>0) {
    Wire.read();
    flag="1\n";
  }
}
