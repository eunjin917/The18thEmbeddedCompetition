//아두이노간에 I2C 통신방식을 이용

#define SHOCK 8 //핀 설정(디지털신호 받는 핀)\

void setup() {
  Serial.begin(9600);//PC모니터로 센서값을 확인하기위해서 시리얼 통신을 정의해줍니다.
                      //시리얼 통신을 이용해 PC모니터로 데이터 값을 확인하는 부분은 자주사용되기 때문에
                      //필수로 습득해야하는 교육코스 입니다.
  pinMode(SHOCK, INPUT);
}

void loop() {
  //아두이노에 데이터 전송
  if (digitalRead(SHOCK) != HIGH) {
    Serial.write(1);
  }
}
