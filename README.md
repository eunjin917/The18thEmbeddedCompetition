# The 18th embedded competition

## Requirements

* Python >= 3.6

## Project Setting
**git bash에서 수행**

* Clone from Github
```
// You **MUST** work in a clean directory.
$ git clone https://gitlab.com/NPclown/the-18th-embedded-competition.git
$ cd the-18th-embedded-competition // D:\the-18th-embedded-competition\
```

* Install django
```
$ cd web // D:\the-18th-embedded-competition\web
$ pip install django
```

* Setting ENV
  * copy `venv`
  ```
  $ python -m venv myvenv
  ```

  * Acitvate `venv`
  ```
  $ . myvenv/Scripts/activate //windows
  ```
  
## Local Dev Server
```
// web server
$ cd myproject // D:\the-18th-embedded-competition\web\myproject
$ python manage.py runserver

// user
https://127.0.0.1:8000

// admin
https://127.0.0.1:8000/admin
ID : admin@admin.admin, PW : embedded

// 주변 차량 확인하기 기능
- the-18th-embedded-competition\web\data.txt를 upload
- 형식
MAC주소12자리
/날짜
주변MAC주소12자리
...
/날짜
주변MAC주소12자리
...
```