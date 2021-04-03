from datetime import datetime
from flask import render_template
from logs.detail import error_log
import pymysql


def connectsql():
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='0000', db='todolist', charset='utf8')
        return conn
    except pymysql.DatabaseError as e:
        code, msg = e.args
        print("connectionError : {}".format(e))
        time = datetime.now()
        res = "TIME : {0}, CODE : {1}, MSG : {2}".format(time, code, e)
        error_log(res)
        return render_template('dberror.html')


def query_excute_with_value(query, value):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, value)
    conn.commit()
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def query_excute_only_query(query):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
