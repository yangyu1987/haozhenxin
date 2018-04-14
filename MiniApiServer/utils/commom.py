# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/10
import random,hashlib,os,json,requests,re,time
# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def sms6num():
    # 短信验证码生成器
    numbers = ''
    for i in range(6):
        numbers += str(random.randint(0, 9))
    return numbers


def creToken():
    #token 生成器
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    return token


def timeCheckForCookie(old,timeline):
    # old 毫秒级时间戳
    #timeline 分钟数
    bt = time.time()*1000 - int(old)
    if bt/86400000>timeline:
        return False # 超过时间跨度
    else:
        return True # 在时间跨度内


def timeCheckForToken(old,timeline):
    # old 毫秒级时间戳
    #timeline 天数
    bt = time.time()*1000 - int(old)
    if bt/60000>timeline:
        return False # 超过时间跨度
    else:
        return True # 在时间跨度内


def zx_test(name,idCard,mobile,servicename,post_url):
    headers = {
        "Content-Type": "Application/json;charset=utf-8",
    }
    if servicename == "PaymentBlackVerify":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    elif servicename == "RiskListCombineInfo":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    elif servicename == "BlackListCheck":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    else:
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile':mobile
        }

    params = {
        "loginName": "xyh123456",
        "pwd": "xyh123456",
        "serviceName": servicename,
        "param": postParam
    }
    payload = json.dumps(params)
    res = requests.post(post_url, data=payload, verify=False)

    return res.text


def csrfJsonRes(HttpResponse,msg_res):
    # 
    response = HttpResponse(json.dumps(msg_res))
    response['Content-Type'] = "application/json"
    response['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == "__main__":
    old = '1523587852000'
    print(timeCheckForToken(old,26))