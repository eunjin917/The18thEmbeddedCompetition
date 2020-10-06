### HM-10 Firmware Update

< 주의 >
HM-10은 5V로 연결하지만 CC2541로 연결할 경우 3.3V로 연결

< 커맨드 명령어 >
CCLoader.exe 5 CC2541hm10v540.bin 0  
( CCLoader.exe <COM Port> <FirmwareFile.bin> 0 )

< 참조 영상 >
https://youtu.be/ez3491-v8Og


### AT-Command Explain

* AT+HELP : AT 커맨드 목록 
* AT : Bluetooth Module을 확인할 때 사용한다.
* AT+LADDR? : Bluetooth Module의 MAC주소를 확인하는데 사용한다.
* AT+NAME? : Master Device가 Bluetooth Module을 검색할 때 어떤 이름인지 확인하는데 사용한다.
* AT+TYPE? : Bluetooth Module가 어떤 타입을 사용하는지 확인하는데 사용한다. 보통 1번이 default로 되어있는데 3번으로 바꿔야 안드로이드와 연결이 된다.
* AT+MODE? : Bluetooth 통신 방법 중 “Connection”인지 “Broadcast”인지 확인한다. Connection이 보통 사용하는 방법이고 Broadcast가 “Beacon”이다.
* AT+RESET : 재시작할 때 사용한다.
* AT+RENEW : 공장초기화 할 때 사용한다.
* AT+BAUD보레이트메뉴값.
    1 - 1200,  2 - 2400, 3 - 4800,  4 - 9600,  5 - 19200,  6 - 38400, 7 - 57600,  8 - 115200 
    
    
< 참조 웹 >
1. http://blog.naver.com/PostView.nhn?blogId=xisaturn&logNo=220712028679

