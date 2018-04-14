from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from haozx import models
from haozx.tools import sendmsg
from utils.commom import *
from utils.config import *
import uuid,json,time
from concurrent.futures import ThreadPoolExecutor
# Create your views here.


class TokenMaker(View):
    # 访问页面挂载token
    def get(self, request):
        tokens = models.Tokens()
        token= creToken()
        tokens.token = token
        tokens.timestamp = int(time.time() * 1000)
        tokens.save()
        msg_res = {
            'token': token,
        }
        response = HttpResponse(json.dumps(msg_res))
        response['Content-Type'] = "application/json"
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def post(self, request):
        # 访问页面挂载token
        tokens = models.Tokens()
        token = creToken()
        tokens.token = token
        tokens.timestamp = int(time.time() * 1000)
        tokens.save()
        msg_res = {
            'token': token,
        }
        response = HttpResponse(json.dumps(msg_res))
        response['Content-Type'] = "application/json"
        response['Access-Control-Allow-Origin'] = "*"
        return response


class Sendmsg(View):
    # 短信发送模块
    def get(self, request):
        return render(request, 'haozx/sendmsg.html')
        # return HttpResponse('短信输入页面')

    def post(self, request):
        # 校验和发送
        phoneNum = request.POST.get('phoneNum', '')
        token = request.POST.get('token', '')
        smsCode = sms6num() # 短信验证码
        # 校验token 是否存在
        try:
            # token 校验成功
            token_sql = models.Tokens.objects.get(token=token)
            if timeCheckForToken(token_sql.timestamp, 30):
                # token时间30分钟内
                try:
                    # 检查库中是否有手机号，有说明查过了 更新数据
                    hzx = models.Haozx.objects.get(phoneNum=phoneNum,codeUsed=1)
                    hzx.smsCode = smsCode
                    # 发送短信
                    __business_id = uuid.uuid1()
                    params = json.dumps({'code': smsCode})
                    dy_res = sendmsg.send_sms(__business_id, phoneNum, "好甄信", "SMS_130915678", params)
                    dy_res = json.loads(dy_res)
                    if dy_res['Code'] == "OK":
                        # "Code": "OK" 表示发送成功
                        hzx.smsSend = 1  #
                        hzx.codeUsed = 0 # 把短信验证状态置为零
                        # hzx.timestamp = int(time.time() * 1000)  # 不在记录发送时间
                        hzx.save()
                        msg_res = {
                            'success': 1,
                            'info': 'Sms send suc',
                            'phoneNum': phoneNum,
                            'token': token
                        }
                        response = HttpResponse(json.dumps(msg_res))
                        response['Content-Type'] = "application/json"
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
                    else:
                        hzx.smsSend = 0
                        hzx.save()
                        msg_res = {
                            'success': 0,
                            'info': 'Sms send Fail',
                        }
                        response = HttpResponse(json.dumps(msg_res))
                        response['Content-Type'] = "application/json"
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
                except:
                    # 库中无查询记录 新建数据
                    hzx = models.Haozx()
                    # 在记录表中存入手机号和短信验证码
                    hzx.phoneNum = phoneNum
                    hzx.smsCode = smsCode
                    # 发送短信
                    __business_id = uuid.uuid1()
                    params = json.dumps({'code': smsCode})
                    dy_res = sendmsg.send_sms(__business_id, phoneNum, "好甄信", "SMS_130915678", params)
                    dy_res = json.loads(dy_res)
                    if dy_res['Code'] == "OK":
                        # "Code": "OK" 表示发送成功
                        hzx.smsSend = 1
                        # hzx.timestamp = int(time.time() * 1000) # 发送时间 时间统一在查询时候记录
                        hzx.save()
                        msg_res = {
                            'success': 1,
                            'info': 'Sms send suc',
                            'phoneNum':phoneNum,
                            'token': token
                        }
                        response = HttpResponse(json.dumps(msg_res))
                        response['Content-Type'] = "application/json"
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
                    else:
                        hzx.smsSend = 0
                        hzx.save()
                        msg_res = {
                            'success': 0,
                            'info': 'Sms send Fail',
                        }
                        response = HttpResponse(json.dumps(msg_res))
                        response['Content-Type'] = "application/json"
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
            else:
                # token 过期
                msg_res = {
                    'success': 0,
                    'info': 'Token Time Out',
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
        except:
            # token 校验失败
            msg_res = {
                'success': 0,
                'info': 'NO such Token',
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response


class Checkmsg(View):
    # 短信校验模块
    def get(self, request):
        return render(request, 'haozx/checkmsg.html')
        # return HttpResponse('输入页面')

    def post(self, request):
        phoneNum = request.POST.get('phoneNum', '')
        smsCode = request.POST.get('smsCode', '')
        token = request.POST.get('token', '')
        token_sql = models.Tokens.objects.get(token=token)
        if timeCheckForToken(token_sql.timestamp, 30):
            # 开始校验
            try:
                hzx = models.Haozx.objects.get(phoneNum=phoneNum,smsCode=smsCode)
                # 校验成功把校验状态设为1
                hzx.codeUsed = 1
                hzx.save()
                msg_res = {
                    'success': 1,
                    'info': 'Sms Check Suc',
                    'phoneNum':phoneNum,
                    'token':token
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
            except:
                msg_res = {
                    'success':0,
                    'info':'Sms Check Fail'
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
        else:
            # token 过期
            msg_res = {
                'success': 0,
                'info': 'Token Time Out',
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response


class GetRes(View):
    # 接口查询 并返回结果
    def get(self, request):
        return render(request, 'haozx/getmaininfo.html')
        # return HttpResponse(status=503)

    def post(self, request):
        # 5线程查询5个接口
        name = request.POST.get('name', '')
        idCard = request.POST.get('idCard', '')
        phoneNum = request.POST.get('phoneNum', '')
        token = request.POST.get('token', '')
        sernames = SERVICENAMES
        # 验证token 是否过期
        token_sql = models.Tokens.objects.get(token=token)
        if timeCheckForToken(token_sql.timestamp, 30):
            # 未过期 开始主查询线
            try:
                # sql_res = models.Haozx.objects.get(token=token, codeUsed=0) # 检测验证码是否用过
                sql_res = models.Haozx.objects.get(phoneNum=phoneNum,codeUsed=1) # 说明短信验证已通过
            except:
                msg_res = {
                    'success': 0,
                    'info': 'error'
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response

            # 已有缓存数据 时间不超过1个月
            if sql_res.result and timeCheckForCookie(sql_res.timestamp, 30):
                # 暴露结果
                msg_res = {
                    'success': 1,
                    'data': sql_res.result
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response

            # 没有缓存数据或缓存时间大于一个月去接口查询
            else:
                sql_res.name = name
                sql_res.idCard = idCard
                mobile = str(sql_res.phoneNum)
                # 多线程
                executor = ThreadPoolExecutor(max_workers=5)
                res_dic = {}
                for s, u in sernames.items():
                    res = executor.submit(zx_test, *(name, idCard, mobile, s, u))
                    res_dic[s] = res.result()
                # 获取返回结果
                sql_res.result = json.dumps(res_dic)
                # 更新验证码为已用
                sql_res.codeUsed = 1
                sql_res.timestamp = int(time.time() * 1000)
                sql_res.save()
                # 暴露结果
                response = HttpResponse(json.dumps(res_dic))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
        else:
            # token 过期
            msg_res = {
                'success': 0,
                'info': 'Token Time Out',
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response