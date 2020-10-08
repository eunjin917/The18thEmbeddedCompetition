// DS1302_Serial_Easy 
// Copyright (C)2015 Rinky-Dink Electronics, Henning Karlsen. All right reserved
// web: http://www.RinkyDinkElectronics.com/
//
// A quick demo of how to use my DS1302-library to 
// quickly send time and date information over a serial link
//
// I assume you know how to connect the DS1302.
// DS1302:  RST pin   -> Arduino Digital 5
//          I/O pin   -> Arduino Digital 6
//          SCLK pin  -> Arduino Digital 7

#include "Arduino.h"
#include "TIME.h"
#include "DS1302.h"
#define RST_PIN 5
#define IO_PIN 6
#define SCLK_PIN 7
DS1302 rtc(RST_PIN, IO_PIN, SCLK_PIN);
Time t;

void DS1302_Start () {//수정 방지모드로 설정후 모듈 시작
  rtc.halt(false); // 동작 모드로 설정
  rtc.writeProtect(true); // 쓰기 방지 설정 비활성화(false), ture이면 수정 불가능
}

String now(){ // 2020년09월25일  17시00분07초 형식으로 출력
  t=rtc.getTime();
  int M1=t.mon;
  int D=t.date;
  int H=t.hour;
  int M2=t.min;
  int S=t.sec;
  String y,m1,d,h,m2,s;

  y=String(t.year);
  m1=M1<10 ? "0"+String(M1) : String(M1);
  d=D<10 ? "0"+String(D) : String(D);
  h=H<10 ? "0"+String(H) : String(H);
  m2=M2<10 ? "0"+String(M2) : String(M2);
  s=S<10 ? "0"+String(S) : String(S);

  return y+"년"+m1+"월"+d+"일\t"+h+"시"+m2+"분"+s+"초";
}

void time_setting(String t, String d){//아두이노에서 시간을 받아와서 DS1302에 시간 설정
  rtc.halt(false); // 동작 모드로 설정
  rtc.writeProtect(false); // 쓰기 방지 설정 비활성화(false), ture이면 수정 불가능

  //__TIME__ -> t "Feb 24 2011"형식으로 read
  int first = t.indexOf(":"); // 첫번째 콤마위치
  int second = t.indexOf(":",first+1); // 두번째 콤마 위치
  String str1 = t.substring(0, first); // 첫번째 토큰
  String str2 = t.substring(first+1, second); // 두번째 토큰
  String str3 = t.substring(second+1,t.length()); // 세번째 토큰

  rtc.setTime(str1.toInt(), str2.toInt(), str3.toInt()); // 시간 설정 (24시간 형식)


  //__DATE__ -> d "19:20:28"형식으로 read
  first = d.indexOf(" ");
  second = d.indexOf(" ",first+1);
  str1 = d.substring(0, first); // 첫번째 토큰
  str2 = d.substring(first+1, second); // 두번째 토큰
  str3 = d.substring(second+1,d.length()); //세번째 토큰
  int month;
  if(str1.compareTo("Jan")==0){
    month=1;
  }
  else if(str1.compareTo("Feb")==0){
    month=2;
  }
  else if(str1.compareTo("Mar")==0){
    month=3;
  }
  else if(str1.compareTo("Apr")==0){
    month=4;
  }
  else if(str1.compareTo("May")==0){
    month=5;
  }
  else if(str1.compareTo("Jun")==0){
    month=6;
  }
  else if(str1.compareTo("Jul")==0){
    month=7;
  }
  else if(str1.compareTo("Aug")==0){
    month=8;
  }
  else if(str1.compareTo("Sep")==0){
    month=9;
  }
  else if(str1.compareTo("Oct")==0){
    month=10;
  }
  else if(str1.compareTo("Nov")==0){
    month=11;
  }
  else if(str1.compareTo("Dec")==0){
    month=12;
  }
  
  rtc.setDate(str2.toInt(), month, str3.toInt()); // 날짜 설정
}
