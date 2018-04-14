from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from haozx import models
from haozx.tools import sendmsg
from utils.commom import *
from utils.config import *
import uuid,json,time
from concurrent.futures import ThreadPoolExecutor
from .forms import CaptchaTestForm
# Create your views here.


class TokenMaker(View):
    # 访问页面挂载token
    def get(self, request):
        haozx = models.Haozx()
        token = creToken()
        haozx.token = token
        haozx.save()
        msg_res = {
            'token': token,
        }
        return JsonResponse(msg_res)


class Sendmsg(View):
    # 短信发送模块
    def get(self, request):
        captcha = CaptchaTestForm()
        return render(request, 'haozx/sendmsg.html',{'captcha':captcha})
        # return HttpResponse('短信输入页面')

    def post(self, request):
        # 载入数据模型
        haozx = models.Haozx()
        phoneNum = request.POST.get('phoneNum', '')
        smsCode = sms6num() # 短信验证码
        token = creToken()
        # 存入验证码 token phonenum smsCode
        haozx.phoneNum = phoneNum
        haozx.smsCode = smsCode
        haozx.timestamp = int(time.time() * 1000)
        haozx.token = token
        # 发送短信
        __business_id = uuid.uuid1()
        params = json.dumps({'code':smsCode})
        dy_res = sendmsg.send_sms(__business_id, phoneNum, "好甄信", "SMS_130915678", params)
        dy_res = json.loads(dy_res)
        if dy_res['Code'] == "OK":
            # "Code": "OK" 表示发送成功
            haozx.smsSend = 1
            haozx.save()
            msg_res = {
                'success': 1,
                'info': '短信发送成功',
                'token': token
            }
            return JsonResponse(msg_res)
        else:
            haozx.smsSend = 0
            haozx.save()
            msg_res = {
                'success': 0,
                'info': '短信发送失败',
            }
            return JsonResponse(msg_res)


class Checkmsg(View):
    # 短信校验模块
    def get(self, request):
        return render(request, 'haozx/checkmsg.html')
        # return HttpResponse('输入页面')

    def post(self, request):
        phoneNum = request.POST.get('phoneNum', '')
        smsCode = request.POST.get('smsCode', '')
        token = request.POST.get('token', '')
        # 开始校验
        try:
            sql_res = models.Haozx.objects.get(phoneNum=phoneNum,smsCode=smsCode,token=token,codeUsed=0)
            msg_res = {
                'success': 1,
                'info': '短信校验成功'
            }
            return JsonResponse(msg_res)
        except:
            msg_res = {
                'success':0,
                'info':'短信校验失败'
            }
            return JsonResponse(msg_res)


class GetRes(View):
    # 接口查询 并返回结果
    def get(self, request):
        return render(request, 'haozx/getmaininfo.html')
        # return HttpResponse(status=503)

    def post(self, request):
        # 5线程查询5个接口
        name = request.POST.get('name', '')
        idCard = request.POST.get('idCard', '')
        token = request.POST.get('token', '')
        sernames = SERVICENAMES
        #开始访问
        try:
            sql_res = models.Haozx.objects.get(token=token, codeUsed=0)
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
            sql_res.save()
            # 暴露结果
            return JsonResponse(res_dic)
        except:
            msg_res = {
                'success': 0,
                'info': '非法访问'
            }
            return JsonResponse(msg_res)