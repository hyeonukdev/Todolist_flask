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

def connectsql():
    conn = pymysql.connect(host='localhost',port=3306, user='root', passwd='0000', db='todolist', charset='utf8')
    return conn

def create_tables():
    # connection()
    global cursor
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
    # sql = """CREATE TABLE user(
    #              id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #              user_id VARCHAR(30) NOT NULL,
    #              user_pw VARCHAR(20) NOT NULL,
    #              user_name VARCHAR(10) NOT NULL,
    #              recent_login VARCHAR(20)
    #              );"""

    # 최근 로그인 쿼리
    # sql = """
    #     ALTER TABLE user
    #         ADD recent_login VARCHAR(20);
    # """


    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "ALTER TABLE user MODIFY user_pw varchar(100);"
    # query = "ALTER TABLE board convert to charset utf8;"
    # query = "ALTER  board MODIFY upload varchar(50);"
    # query = "ALTER TABLE board MODIFY upload varchar(50);"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    return print("SUCCESS CREATE TABLE")




#---------
create_tables()