# Todo List
### Function
- 게시판
    1. 게시글 작성
    2. 게시글 수정
    3. 게시글 삭제
- 회원
    1. 회원 가입
       - bcrypt hash regist
    2. 회원 수정
    3. 회원 탈퇴

### Database 
- Board
    1. Num
    2. Title
    3. Content
    4. Author
    5. created_date
    6. Count views
    7. Upload File
        - Only Image
- Login
    1. id
    2. pw
    3. username
    4. Recent login record
    5. master auth
        - username이 master이면 전체 post view
        - 단, 수정은 불가 / 삭제는 가능 
    
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
### 작성일 : 2021.04.03.
### 문서버전 : v1.2.0
---