import re

def ip_check(ip):
    url = ip.split(':', 1)[0]
    # print(url)

    p = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    res = re.search(p, url)
    if res is not None:
        # print("valid")
        return True
    else:
        # print("Invalid")
        return False

#---
ip_check('127.0.0.1:8000')