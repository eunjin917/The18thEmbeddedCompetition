# HardWare

## Setting

Bluetooth

```
블루투스 초기 설정을 위한 코드

  //공장 초기화
  HM10.write("AT+RENEW"); 
  
  //HM-10 리붓
  HM10.write("AT+RESET");
  
  //iBeacon의 Major number설정 (0x1234는 임의값 설정 가능)
  HM10.write("AT+AT+MARJ0x1234");
  
  //iBeacon의 Minor number설정 (0xFA02는 임의값 설정 가능)
  HM10.write("AT+MINO0xFA02");
  
  //advertising(신호 송출) 주기를 5로 설정(약 0.5초)
  HM10.write("AT+ADVI5");//number 표기
  
  //HM-10 이름 정의 ( Dolphin[number] )
  HM10.write("AT+NAMEDolphin");
  
  //전원 절약을 위해 맺지않음(non-connectable)모드로 설정
  HM10.write("AT+ADTY3");
  
  //iBeacon을 활성화
  HM10.write("AT+IBEA1");
  
  //iBeacon의 broadcast-only 로 설정
  HM10.write("AT+DELO2");
  
  //전원 절약을 위해 auto-sleep으로 설정(최소 절전 모드)
  HM10.write("AT+PWRM0");
  
  //리붓하여 반영
  HM10.write("AT+RESET");

```

HM-10
```
HM-10 초기 설정을 위한 코드

- 정품이 아닌 CCLoader를 활용한 Firmware Updater가 필요한다.
- 그 이후 HM-10 Setting 코드를 실행한다.

```
## Main (실제 동작 소스코드)

1. 첫번째 아두이노 미니에 "Bluetooth_Device_Discovery" 코드를 업로드 후 실행 시킨다.
2. 두번째 아두이노 미니에 "Shock_Detect_Sensor" 코드를 업로드 후 실행 시킨다.
3. 브레드보드에 두 아두이노 미니를 연결한다.