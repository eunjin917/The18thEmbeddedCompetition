#include <SoftwareSerial.h>
#include "Time.h"

#define BT_RX 2  // HM-10의 TX에 연결
#define BT_TX 3  // HM-10의 RX에 연결
#define vendor_code "341513" // vendor code
#define device_name "Dolphin" // device name

SoftwareSerial HM10(BT_RX,BT_TX);

void setup(){
  Serial.begin(9600); // 전송속도 설정
  HM10.begin(9600);
  /*--------------------------
  -> DS1302 시간 설정할떄만 사용
  time_setting(__TIME__);
  */--------------------------
  DS1302_Start();
}
 
void loop(){
  HM10.write("AT+DISC?");
  if (HM10.find((char*)"OK+DIS0:")){//주소를 쿼리
    String str=HM10.readString();
    Serial.print(String_cleanup(str));
  }
}

String String_cleanup(String str){ //쿼리문 깔끔하게 정리
  String newStr="";
  String newTime="\t"+now();//현재시간
  
  str.replace("OK+DIS0:","");
  str.replace("OK+DIS1:","");
  str.replace("OK+DIS2:","");
  str.replace("OK+NAME:"," ");

  //한줄씩 받아서 필터처리
  while(str!=""){
    String temp=str.substring(0,str.indexOf('\n'));
    if(temp.substring(0,6)==vendor_code && temp.substring(13,20)==device_name){
      temp.concat(" "+newTime);
      newStr+=temp+'\n';
    }
    str=str.substring(str.indexOf('\n')+1);
  }
  return newStr;
}
