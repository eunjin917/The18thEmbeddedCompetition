//아두이노간에 I2C 통신방식을 이용
#include <Wire.h>

#define SHOCK 8 //핀 설정(디지털신호 받는 핀)

void setup() {
  Serial.begin(9600);
  Wire.begin();
  pinMode(SHOCK, INPUT);
}

void loop() {
  //아두이노에 데이터 전송/
  Wire.beginTransmission(8);
  if (digitalRead(SHOCK) != HIGH) { // 충격을 감지했을 때
    Wire.write(1); // 충격을 받았다고 신호 전송
  }
  Wire.endTransmission();
}
