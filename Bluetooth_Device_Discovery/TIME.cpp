// CONNECTIONS:
// DS1302 CLK/SCLK --> 5
// DS1302 DAT/IO --> 4
// DS1302 RST/CE --> 3
// DS1302 VCC --> 3.3v - 5v
// DS1302 GND --> GND
#include "Arduino.h"
#include "TIME.h"
#include <DS1302.h>
#define CLK_PIN 7 //SCLK_PIN
#define DAT_PIN 6 //IO_PIN
#define RST_PIN 5
DS1302 rtc(RST_PIN, DAT_PIN, CLK_PIN);
Time t;

void DS1302_Start () {//수정 방지모드로 설정후 모듈 시작
  rtc.halt(false); // 동작 모드로 설정
  rtc.writeProtect(true); // 쓰기 방지 설정 비활성화(false), ture이면 수정 불가능
}

String now(){//현재시간 YYYY-MM-DD 형식으로 출력
  t = rtc.getTime();
  return String(t.year)+"-"+String(t.mon)+"-"+String(t.date)+" "+rtc.getTimeStr();
}

void time_setting(String str){//아두이노에서 시간을 받아와서 DS1302에 시간 설정
  rtc.halt(false); // 동작 모드로 설정
  rtc.writeProtect(false); // 쓰기 방지 설정 비활성화(false), ture이면 수정 불가능

  int first = str.indexOf(":"); // 첫번째 콤마위치
  int second = str.indexOf(":",first+1); // 두번째 콤마 위치
  int strlength = str.length(); // 문자열 길이
  String str1 = str.substring(0, first); // 첫번째 토큰
  String str2 = str.substring(first+1, second); // 두번째 토큰
  String str3 = str.substring(second+1,strlength); // 세번째 토큰
    
  //rtc.setDOW(SUNDAY); // 요일 설정
  rtc.setTime(str1.toInt(), str2.toInt(), str3.toInt()); // 시간을 12:00:00로 설정 (24시간 형식)
  rtc.setDate(29, 8, 2020); // 2020년 8월 29일로 설정
}
