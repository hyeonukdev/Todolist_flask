# Todo List
### Function
- 게시판
    [x]1. 게시글 작성
    [x]2. 게시글 수정
    [x]3. 게시글 삭제
- 회원
    [x]1. 회원 가입
    [x]2. 회원 수정
    []3. 회원 탈퇴

### Database 
- Board
    [x]1. id
    [x]2. Title
    [x]3. Content
    [x]4. Author
    [x]5. Count views
    [x]6. created_date
    []7. Upload File
        - Only Image
- Login
    [x]1. id
    [x]2. pw
    []3. Recent login record
    
### Restrictions
- Flask blueprint method를 사용해서 endpoint 구분하기
- SSR 서버사이드렌더링 사용
- ORM 사용 X
- Login
    - flask beaker 사용
    - flask run 명령어 사용 X
- Security
    - 크로스 사이트 스크립트 방지(XSS)
    - SQL Injection 방지
- LOG
    1. DETAIL_INFO
        - Time
        - ip
        - login user_id
        - Data
        - URL
    2. ERROR
        - ERROR msg
        - Traceback
    3. Access information
---
## Environment 
- Framework : Flask
- Database : MySQL
- Server : nginx
---
## 작성자 : 강현욱
### 작성일 : 2021.02.22.
### 문서버전 : v0.0.3
---