//아두이노간에 I2C 통신방식을 이용
#include <Wire.h>

#define SHOCK 8 // 충돌감지 센서 핀 설정(디지털신호 받는 핀)

void setup() {
  Serial.begin(9600);
  Wire.begin();
  pinMode(SHOCK, INPUT);
}

void loop() {
  Wire.beginTransmission(8);// address는 8
  if (digitalRead(SHOCK) != HIGH) { // 충돌이 발생하면 데이터를 송신
    Wire.write(1);
  }
  Wire.endTransmission();
}
