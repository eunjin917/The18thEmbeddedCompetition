int LED_Pin = 13;
int vibr_Pin =3;

void setup(){
  pinMode(LED_Pin, OUTPUT);
  pinMode(vibr_Pin, INPUT); //set vibr_Pin input for measurment
  Serial.begin(9600); //init serial 9600
 // Serial.println("----------------------Vibration demo------------------------");
}
void loop(){
  long measurement = TP_init();
  delay(50);
  if(measurement > 0 ){
    Serial.println("SHOCK!!");
  }
}

long TP_init(){
  delay(10);
  long measurement=pulseIn (vibr_Pin, HIGH);  //wait for the pin to get HIGH and returns measurement
  return measurement;
}
