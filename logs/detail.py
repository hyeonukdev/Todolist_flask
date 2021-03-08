import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN_DIR = os.path.join(ROOT_DIR, 'login.log')
DETAIL_DIR = os.path.join(ROOT_DIR, 'detail.log')
ERROR_DIR = os.path.join(ROOT_DIR, 'error.log')


def login_log(res):
    f = open(LOGIN_DIR, mode='at', encoding='utf-8')
    f.write("\n")
    f.writelines(res)
    f.close()
    return print("저장된 LOG {}".format(res))


def detail_log(res):
    f = open(DETAIL_DIR, mode='at', encoding='utf-8')
    f.write("\n")
    f.writelines(res)
    f.close()
    return print("저장된 LOG {}".format(res))

def error_log(res):
    f = open(ERROR_DIR, mode='at', encoding='utf-8')
    f.write("\n")
    f.writelines(res)
    f.close()
    return print("저장된 LOG {}".format(res))


def get_client_ip(request):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return ip

