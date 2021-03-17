from datetime import datetime
from logs.detail import login_log, get_client_ip, detail_log, error_log
from flask import Flask, flash, render_template, session, url_for, request, redirect, send_from_directory, escape
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