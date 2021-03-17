import os
from flask import Flask, flash, render_template, session, url_for, request, redirect, send_from_directory, escape
from werkzeug.utils import secure_filename
from flask import Blueprint
import pymysql
from datetime import datetime
import app
import bcrypt
from util.password import password_check
from util.connetsql import connectsql
from util.check_ip import ip_check

from logs.detail import login_log, get_client_ip, detail_log, error_log

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('main', __name__, url_prefix='/')


# ----------
@bp.route('/')
def index():
    if 'username' in session:
        username = session['username']

        return render_template('index.html', logininfo=username)
    else:
        return render_template('Error.html')


@bp.route('/post', methods=['GET'])
def post():
    if 'username' in session:
        username = session['username']
    else:
        username = None
        return render_template('Error.html')

    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if username == 'master':
        query = "SELECT id, title, content, author, wdate, udate, view FROM board"
        cursor.execute(query)
    else:
        query = "SELECT id, title, content, author, wdate, view FROM board WHERE author= %s ORDER BY id DESC"
        value = username
        cursor.execute(query, value)
    post_list = cursor.fetchall()

    cursor.close()
    conn.close()

    url = request.url
    ip = get_client_ip(request)
    try:
        ip_check(ip)
    except Exception as e:
        print(e)
    else:
        wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
        content = "post Page"
        # LOG
        res = "TIME : {0}, IP : {1}, LOGIN_USER : {2}, DATA : {3}, URL : {4}".format(wdate, ip, username, content, url)
        detail_log(res)

        return render_template('post.html', postlist=post_list, logininfo=username)


@bp.route('/post/content/<id>', methods=['GET'])
def content(id):
    if 'username' in session:
        # 조회수 +=1
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "UPDATE board SET view = view + 1 WHERE id = %s"
        value = id
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        # post 정보
        conn = connectsql()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = "SELECT id, title, content, author, wdate, udate, view FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)

        content = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        # print("content : {}".format(content))
        author = content[0]['author']
        # print("author : {}".format(author))

        if username == 'master':
            pass
        elif username != author:
            return render_template('NotmatchingUser.html')

        # 이미지 정보
        conn = connectsql()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT upload FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        img_name = cursor.fetchall()
        img_name = img_name[0]['upload']

        conn.commit()
        cursor.close()
        conn.close()

        url = request.url
        ip = get_client_ip(request)
        wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))

        # LOG
        res = "TIME : {0}, IP : {1}, LOGIN_USER : {2}, DATA : {3}, URL : {4}, IMG : {5}".format(wdate, ip, username,
                                                                                                content, url, img_name)
        detail_log(res)

        return render_template('content.html', data=content, username=username, img_name=img_name)
    else:
        return render_template('Error.html')


@bp.route('/post/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']

            edittitle = request.form['title']
            editcontent = request.form['content']

            udate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            image_name = request.form['file']

            if image_name != "":
                filename = image_name

                count_id = id
                filename, file_ext = os.path.splitext(filename)

                file_date = str(datetime.today().strftime("%Y%m%d"))
                upload = str(count_id) + "_" + filename + "_" + file_date + file_ext

            conn = connectsql()
            cursor = conn.cursor()

            if image_name:
                query = "UPDATE board SET title = %s, content = %s, udate = %s, upload = %s WHERE id = %s"
                value = (edittitle, editcontent, udate, upload, id)
            else:
                query = "UPDATE board SET title = %s, content = %s, udate = %s WHERE id = %s"
                value = (edittitle, editcontent, udate, id)

            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            url = request.url
            ip = get_client_ip(request)
            wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            # LOG
            res = "TIME : {0}, IP : {1}, LOGIN_USER : {2}, DATA : {3}, URL : {4}".format(wdate, ip, username, value,
                                                                                         url)
            detail_log(res)

            return render_template('editSuccess.html')
    else:
        if 'username' in session:
            username = session['username']
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT author FROM board WHERE id = %s"
            value = id
            cursor.execute(query, value)
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()

            if username in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, title, content, upload FROM board WHERE id = %s"
                value = id
                cursor.execute(query, value)
                postdata = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('edit.html', data=postdata, logininfo=username)
            else:
                return render_template('editError.html')
        else:
            return render_template('Error.html')


@bp.route('/post/delete/<id>')
def delete(id):
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT author FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        url = request.url
        ip = get_client_ip(request)
        content = "DELETE id-" + value + " in board"
        wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
        # LOG
        res = "TIME : {0}, IP : {1}, LOGIN_USER : {2}, DATA : {3}, URL : {4}".format(wdate, ip, username, content, url)
        detail_log(res)

        if username in data:
            return render_template('delete.html', id=id)
        else:
            return render_template('editError.html')
    else:
        return render_template('Error.html')


@bp.route('/post/delete/success/<id>')
def delete_post_success(id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    url = request.url
    ip = get_client_ip(request)
    wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    content = "Delete post id : " + value
    # LOG
    res = "TIME : {0}, IP : {1}, DATA : {2}, URL : {3}".format(wdate, ip, content, url)
    detail_log(res)

    return redirect(url_for('main.post'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_post_id(count_id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "SELECT id FROM board ORDER BY id DESC limit 1"
    cursor.execute(query)
    count_id = cursor.fetchall()
    try:
        count_id = count_id[0][0]
        count_id = count_id + 1
    except:
        count_id = 1

    conn.commit()
    cursor.close()
    conn.close()
    return count_id


# TODO : deleteImage
@bp.route('/imageUpload', methods=['GET', 'POST'])
def upload_file(count_id=None):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename

            count_id = check_post_id(count_id)
            filename, file_ext = os.path.splitext(filename)

            file_date = str(datetime.today().strftime("%Y%m%d"))
            filename = str(count_id) + "_" + filename + "_" + file_date + file_ext

            # TODO : app.config['UPLOAD_FOLDER']
            file.save(os.path.join(app.UPLOAD_DIR, filename))

            url = request.url
            ip = get_client_ip(request)
            wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            # LOG
            res = "TIME : {0}, IP : {1}, filename : {2}, URL : {3}".format(wdate, ip, filename,
                                                                           url)
            detail_log(res)

            return redirect(url_for('main.uploaded_image',
                                    filename=filename))
        else:
            return render_template('imageError.html')
    return render_template('uploadFile.html')


# edit uplaodImage시 id 번호 문제 해결
@bp.route('/imageUpload_edit/<id>', methods=['GET', 'POST'])
def upload_file_edit(id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            # print("------ id : {}".format(id))

            count_id = id
            filename, file_ext = os.path.splitext(filename)

            file_date = str(datetime.today().strftime("%Y%m%d"))
            filename = str(count_id) + "_" + filename + "_" + file_date + file_ext
            # print("------ filename : {}".format(filename))

            # TODO : app.config['UPLOAD_FOLDER']
            file.save(os.path.join(app.UPLOAD_DIR, filename))

            url = request.url
            ip = get_client_ip(request)
            wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            # LOG
            res = "TIME : {0}, IP : {1}, filename : {2}, URL : {3}".format(wdate, ip, filename,
                                                                           url)
            detail_log(res)

            return redirect(url_for('main.uploaded_image',
                                    filename=filename))
        else:
            return render_template('imageError.html')
    return render_template('uploadFile.html')


@bp.route('/display/<filename>')
def uploaded_image(filename):
    # TODO : app.config['UPLOAD_FOLDER']
    return send_from_directory(app.UPLOAD_DIR, filename)


@bp.route('/write', methods=['GET', 'POST'])
def write(count_id=None):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']

            usertitle = request.form['title']
            usercontent = request.form['content']

            wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            view = 0
            upload = None

            image_name = request.form['file']

            if image_name != "":
                filename = image_name

                count_id = check_post_id(count_id)

                filename, file_ext = os.path.splitext(filename)

                file_date = str(datetime.today().strftime("%Y%m%d"))
                upload = str(count_id) + "_" + filename + "_" + file_date + file_ext

            conn = connectsql()
            cursor = conn.cursor()
            query = "INSERT INTO board (title, content, author, wdate, view, upload) values (%s, %s, %s, %s, %s, %s)"
            value = (usertitle, usercontent, username, wdate, view, upload)
            cursor.execute(query, value)
            data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            url = request.url
            ip = get_client_ip(request)

            # LOG
            res = "TIME : {0}, IP : {1}, LOGIN_USER : {2}, DATA : {3}, URL : {4}".format(wdate, ip, username, value,
                                                                                         url)
            detail_log(res)

            return redirect(url_for('main.post'))
        else:
            return render_template('errorpage.html')
    else:
        if 'username' in session:
            username = session['username']

            return render_template('write.html', logininfo=username)
        else:
            return render_template('Error.html')


@bp.route('/logchange', methods=['GET', 'POST'])
def logchange():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            editname = request.form['user_name']
            editpw = request.form['pw']

            conn = connectsql()
            cursor = conn.cursor()
            query = "UPDATE user SET user_name = %s, user_pw = %s WHERE user_id = %s"
            value = (editname, editpw, username)
            cursor.execute(query, value)
            conn.commit()
            data = cursor.fetchall()
            cursor.close()
            conn.close()

            if data:
                conn = connectsql()
                cursor = conn.cursor()
                query = "SELECT user_name FROM user WHERE user_id = %s"
                value = (username)
                username = cursor.execute(query, value)
                data = cursor.fetchall()
                username = data[0][0]

            # LOG
            ip = get_client_ip(request)
            url = request.url
            user_id = '%s' % escape(session['username'])
            wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
            content = "LOGCHANGE editname-" + editname + " editpw-" + editpw
            # LOG
            res = "TIME : {0}, IP : {1}, USER_ID : {2}, DATA : {3}, URL : {4}".format(wdate, ip, user_id, content, url)
            login_log(res)

            return render_template('index.html', username=username)
        else:
            return render_template('logchangeError.html')
    else:
        return render_template('logchange.html')


@bp.route('/logout')
def logout():
    ip = get_client_ip(request)
    url = request.url
    user_id = '%s' % escape(session['username'])

    wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    content = "LOGOUT user_id " + user_id
    # LOG
    res = "TIME : {0}, IP : {1}, USER_ID : {2}, DATA : {3}, URL : {4}".format(wdate, ip, user_id, content, url)
    login_log(res)
    return redirect(url_for('main.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        user_pw = request.form['pw']

        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT user_pw FROM user WHERE user_id = %s"
        value = user_id
        cursor.execute(query, value)
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        row = row[0]
        hashed_pw = row.encode('utf-8')
        user_pw = user_pw.encode('utf-8')

        if bcrypt.checkpw(user_pw, hashed_pw):
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT * FROM user WHERE user_id = %s"
            value = (user_id)
            cursor.execute(query, value)
            data = cursor.fetchall()

            recent_login = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))

            query = "UPDATE user SET recent_login = %s WHERE user_id = %s"
            value = (recent_login, user_id)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            if data:
                session['username'] = request.form['id']
                session['password'] = request.form['pw']

                conn = connectsql()
                cursor = conn.cursor()
                query = "SELECT user_name FROM user WHERE user_id = %s"
                value = user_id
                cursor.execute(query, value)
                data = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()
                username = data[0][0]
                print("username : {}".format(username))

                ip = get_client_ip(request)
                url = request.url

                # LOG
                res = "TIME : {0}, IP : {1}, USER_ID : {2}, URL : {3}".format(recent_login, ip, user_id, url)
                login_log(res)

            return render_template('index.html', username=username)
        else:
            return render_template('loginError.html')
    else:
        return render_template('login.html')


@bp.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        user_id = request.form['id']
        user_pw = request.form['pw']
        user_name = request.form['name']

        pwd_check = password_check(user_pw)

        if pwd_check:
            # PASSWORD HASH
            hashed_pw = bcrypt.hashpw(user_pw.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
            # print(hashed_pw)

            # MYSQL
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT * FROM user WHERE user_id = %s"
            value = user_id
            cursor.execute(query, value)
            data = (cursor.fetchall())
            # import pdb; pdb.set_trace()
            if data:
                return render_template('registError.html')
            else:
                query = "INSERT INTO user (user_id, user_name, user_pw) values (%s, %s, %s)"
                value = (user_id, user_name, hashed_pw)
                cursor.execute(query, value)
                data = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()

                wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
                ip = get_client_ip(request)
                url = request.url
                content = "REGISTER"

                # LOG
                res = "TIME : {0}, IP : {1}, USER_ID : {2}, CONTENT : {3} URL : {4}".format(wdate, ip, user_id, content,
                                                                                            url)
                login_log(res)

                return render_template('registSuccess.html')
        else:
            return render_template('registError_pwd.html')
    else:
        return render_template('regist.html')


@bp.route('/deleteUser')
def deleteUser():
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "DELETE FROM user WHERE user_id = %s"
        value = username
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        wdate = str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
        ip = get_client_ip(request)
        url = request.url
        content = "DELETE USER"

        # LOG
        res = "TIME : {0}, IP : {1}, USER_ID : {2}, CONTENT : {3} URL : {4}".format(wdate, ip, username, content, url)
        login_log(res)

        return render_template('deleteSuccess.html')


@bp.route("/xss", methods=['GET'])
def xss():
    xss_stirng = "<script>alert('flask reflected xss run')</script>"
    return render_template('xss.html', name=xss_stirng)
