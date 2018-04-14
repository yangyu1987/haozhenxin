from django.db import models
from datetime import datetime
# Create your models here.


class Haozx(models.Model):
    # 好甄信
    phoneNum = models.CharField(max_length=255, verbose_name='手机号', default='')
    name = models.CharField(max_length=255, verbose_name='姓名', default='')
    idCard = models.CharField(max_length=255, verbose_name='身份证', default='')
    smsCode = models.CharField(max_length=255, verbose_name='短信验证码', default='')
    smsSend = models.IntegerField(choices=((0, '未发送'), (1, '已发送')), verbose_name='短信是否发送', default=0)
    codeUsed = models.IntegerField(choices=((0, '未使用'), (1, '已使用')), verbose_name='验证码是否已使用', default=0)
    timestamp = models.CharField(max_length=255, verbose_name='请求时间', default='')
    result = models.TextField(verbose_name='查询结果', default='')

    class Meta:
        verbose_name = '好甄信'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '好甄信'


class Tokens(models.Model):
    # 好甄信Token
    token = models.CharField(max_length=255, verbose_name='Token', default='')
    timestamp = models.CharField(max_length=255, verbose_name='生成时间', default='')

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Token'
