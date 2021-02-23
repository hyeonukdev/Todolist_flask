import pymysql

def get_connection():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='todolist_db', charset='utf8')
    return conn