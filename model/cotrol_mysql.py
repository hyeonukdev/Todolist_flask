import pymysql

def connection():
    global db
    db = None
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='0000',
                         db='todolist',
                         charset='utf8')

    global cursor
    cursor = db.cursor()
    print("CONNECTED DATABASE")


def create_tables():
    connection()
    # 게사판 만들기
    # sql = """CREATE TABLE board(
    #          id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #          title VARCHAR(30) NOT NULL,
    #          content VARCHAR(256) NOT NULL,
    #          author VARCHAR(10) NOT NULL,
    #          wdate VARCHAR(20) NOT NULL,
    #          udate VARCHAR(20),
    #          view INT DEFAULT 0,
    #          upload VARCHAR(256)
    #          );"""

    # 사용자 만들기
    sql = """CREATE TABLE user(
                 id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                 user_id VARCHAR(30) NOT NULL,
                 user_pw VARCHAR(20) NOT NULL,
                 user_name VARCHAR(10) NOT NULL,
                 recent_login VARCHAR(20)
                 );"""

    sql = """
        ALTER TABLE user
            ADD recent_login VARCHAR(20);
    """

    # SQL query 실행
    cursor.execute(sql)

    # SQL 반
    db.commit()

    # Database 닫기
    db.close()
    return print("SUCCESS CREATE TABLE")




#---------
create_tables()