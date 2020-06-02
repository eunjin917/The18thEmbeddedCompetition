
## git 사용법

1. gitlab 가입 및 git 설치

    *	[gitlab 가입](https://gitlab.com/)
    *	[git 설치](https://git-scm.com/download/win)
	
2.  git 사용법
	2-1.  작업할 노트북에 폴더 생성

	2-2.  git bash open
	```
	// 깃 사용자 정보 설정
	git init
	git config --global user.name "DongHyun, Son"
	git config --global user.email "nigrumspiritus@gmail.com"
	```
	```
	// 초기 셋팅 (브렌치명(develop)은 각자 입맛대로 자유롭게 사용)
	git remote add origin https://gitlab.com/NPclown/the-18th-embedded-competition.git
	git pull origin master
	git checkout -b develop master
	```
	```
	// 작업 후 
	git status -> 현재 git 상태 확인 
	git add .  -> 현재 모든 파일 or 파일명/폴더명 입력하여 특정 파일 추가
	git commit -m "test" -> commit 내용 입력 후 commit
	git push origin develop -> 원격 저장소 업로드
	```
3.  작업이 끝난 branch는 팀장에게 보고!
	-> 작업이 끝났다는 의미는 해당 브렌치가 독립적으로 컴파일이 가능하다는 것을 의미
	-> README.md 파일을 통해 코드 설명 적기, 웬만하면 코드에 주석을 달리 않고 해석을 가능할 정도로 가독성 높이기

4. Issue 활용
	* 마크다운 방식으로 작성 가능
	* Assignee : 책임자 지정 (코드를 해결해야 할 사람)
	* Milestone : 지금 신경 쓸 필요 없음
	* Labels :  세부 파트에 따라 라벨링 한 후 태그 달기
	*  Due date : 마감일
	*  수정은 가능하지만 삭제는 불가능

5. Wiki로 자료 관리