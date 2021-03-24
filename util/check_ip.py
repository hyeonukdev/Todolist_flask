import re

def ip_check(ip):
    p = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    res = re.search(p, ip)
    if res is not None:
        # print("valid")
        return True
    else:
        # print("Invalid")
        return False
