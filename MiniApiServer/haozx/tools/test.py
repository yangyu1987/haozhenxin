# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/10
import requests,json,re
from concurrent.futures import ThreadPoolExecutor

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def zx_test(name,idCard,mobile,servicename,post_url):
    headers = {
        "Content-Type": "Application/json;charset=utf-8",
    }
    params = {
        "loginName": "xyh123456",
        "pwd": "xyh123456",
        "serviceName": servicename,
        "param": {
            'idCard': idCard,
            'name': name,
            'mobile':mobile
        }
    }
    payload = json.dumps(params)
    res = requests.post(post_url, data=payload, verify=False)

    return res.text


def parse_res(res_dic,new_res,data_type):
    res = json.loads(res_dic['RiskListCombineInfo'])['riskList'][data_type]
    res_code = 0 if res['statCode'] == "2" else 1
    if res_code == 0:
        new_res[data_type]['status'] = 0
    else:
        new_res[data_type]['status'] = 1
        new_res[data_type]['detail'] = res['detailInfo']


if __name__ == '__main__':
    # name = '杨建宇'
    # idCard = '340223198711148117'
    # mobile = '18012981270'
    name = '郝敏敏'
    idCard = '142631199608097017'
    mobile = '18920866363'
    # name = '郝敏敏'
    # idCard = '142631199608097017'
    # mobile = '17835341413'
    # mobile = [
    #     '13247223612',
    #     '18684733398',
    #     '13025989310',
    #     '18683680879',
    #     '13213282345',
    #     '13055585755',
    #     '18627692041',
    #     '13027200790',
    #     '15556188579',
    #     '18652017762',
    #     '15574944412',
    #     '18691687273',
    #     '13298376018',
    #     '13222223648',
    #     '18520377115',
    #     '13013311143',
    #     '13107449000',
    #     '18695016216',
    #     '18659943845',
    #     '13168855287',
    #     '18621748173',
    #     '18602078710',
    #     '18590930060',
    #     '15673948959',
    #     '15506053414',
    #     '15581562222',
    #     '13098643510',
    #     '18649027139',
    #     '18671145606',
    #     '15676474010',
    #     '15610338766',
    #     '15527156586',
    #     '13137736537',
    #     '18607224224',
    #     '18670034947',
    # ]
    sernames = {
        # 'ExecutedInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/ExecutedInfo',
        'PaymentBlackVerify': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/PaymentBlackVerify',
        'RiskListCombineInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/RiskListCombineInfo',
        # 'ExecutedDefaulterInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/ExecutedDefaulterInfo',
        'BlackListCheck': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/BlackListCheck' # 预期黑名单
    }
    # 多线程
    executor = ThreadPoolExecutor(max_workers=5)
    res_dic = {}
    for s,u in sernames.items():
        res = executor.submit(zx_test, *(name,idCard,mobile,s,u))
        res_dic[s] = res.result()

    # print(res_dic)
    # data_PaymentBlackVerify = res_dic.get('PaymentBlackVerify')
    # data_RiskListCombineInfo = res_dic.get('RiskListCombineInfo')
    # data_BlackListCheck = res_dic.get('BlackListCheck')
    # print(type(data_PaymentBlackVerify))
    # print(data_PaymentBlackVerify)
    # print(data_RiskListCombineInfo)
    # print(data_BlackListCheck)
    # data_cuishou = re.search(''PaymentBlackVerify" : "\*\d+/(.*)}"', str(res_dic)).group(1)
    common_stat = int(json.loads(res_dic.get('BlackListCheck'))['RESULT'])
    if common_stat < 0:
        print(common_stat)
        print('号码类型错误')
    else:
        new_res = {
            'PaymentBlackVerify': 0,
            'BlackListCheckint': 0,
            'courtDefaulter':{
                'status':2,
                'detail':''
            },
            'bankOverdue': {
                'status': 2,
                'detail': ''
            },
            'netLoanOverdue': {
                'status': 2,
                'detail': ''
            },
            'longLoanApply': {
                'status': 2,
                'detail': ''
            },
            'suspectFraud': {
                'status': 2,
                'detail': ''
            }
        }
        # 开始解析
        # 被催收
        paymentBlackVerify_code = json.loads(res_dic['PaymentBlackVerify'])['detail']['resultCode']
        paymentBlackVerify_code = 0 if paymentBlackVerify_code == "2001" else 1
        new_res['PaymentBlackVerify'] = paymentBlackVerify_code

        # 逾期黑名单
        blackListCheck_code = json.loads(res_dic.get('BlackListCheck'))['RESULT']
        blackListCheck_code = 0 if blackListCheck_code == "2" else 1
        new_res['BlackListCheckint'] = blackListCheck_code

        # 风险详情
        riskListCombineInfo_code = json.loads(res_dic['RiskListCombineInfo'])['RESULT']
        riskListCombineInfo_code = 0 if riskListCombineInfo_code == "2" else 1
        if riskListCombineInfo_code == 0:
            # new_res['RiskListCombineInfo'] = riskListCombineInfo_code
            new_res['courtDefaulter']['status'] = 0 # 行政披露信息
            new_res['bankOverdue']['status'] = 0 # 银行逾期名单信息
            new_res['netLoanOverdue']['status'] = 0 # 网贷逾期名单信息
            new_res['longLoanApply']['status'] = 0 # 多次申贷信息
            new_res['suspectFraud']['status'] = 0  # 疑似欺诈申请信息
        else:
            # 行政披露信息
            parse_res(res_dic,new_res,'courtDefaulter')
            parse_res(res_dic,new_res,'bankOverdue')
            parse_res(res_dic,new_res,'netLoanOverdue')
            parse_res(res_dic,new_res,'longLoanApply')
            parse_res(res_dic,new_res,'suspectFraud')

        print(new_res)




    # headers = {
    #     "Content-Type": "Application/json;charset=utf-8",
    # }
    # params1 = {
    #     "token": "c363ce3624e27d1f6a71876a760e8c48cae4b648",
    #     "phoneNum": "18012981270",
    # }
    # params2 = {
    #     "token": "c363ce3624e27d1f6a71876a760e8c48cae4b648",
    #     "phoneNum": "18012981270",
    #     'smsCode':'173170'
    # }
    # params3 = {
    #     "token": "c363ce3624e27d1f6a71876a760e8c48cae4b648",
    #     "name": "杨宇",
    #     'idCard': '340223198711148117'
    # }
    # post_url = 'http://10.10.1.19:9527/api/bdk/'
    # # res = requests.post(post_url, data=params3)
    # res = requests.post(post_url)
    # print(res.text)
"""
{'PaymentBlackVerify': '{"detail":{"resultCode":"2001","resultMsg":"未命中风险信息"},"guid":"20180414152659_f9C9U58x_1265073","RESULT":"2","MESSAGE":"查询成功，无数据"}', 'RiskListCombineInfo': '{"riskList":{"illegalCheck":{"statCode":"2","statMsg":"无记录"},"courtDefaulter":{"statCode":"2","statMsg":"无记录"},"bankOverdue":{"statCode":"2","statMsg":"无记录"},"netLoanOverdue":{"statCode":"2","statMsg":"无记录"},"longLoanApply":{"statCode":"1","statMsg":"有记录","detailInfo":[{"applyType":"支付公司类","nearHalfMonthCnt":"0","nearMonthCnt":"0","nearWeekCnt":"0","nearSixMonthCnt":"0","applyTime":"2016-12-10 20:03:09,2016-12-10 20:07:49,2017-01-31 00:42:45","nearThreeMonthCnt":"0"},{"applyType":"现金贷类","nearHalfMonthCnt":"0","nearMonthCnt":"0","nearWeekCnt":"0","nearSixMonthCnt":"0","applyTime":"2016-12-25 21:59:25,2017-03-24 21:09:33,2017-03-24 21:09:33","nearThreeMonthCnt":"0"}]},"suspectFraud":{"statCode":"2","statMsg":"无记录"}},"guid":"20180414152700_fN38c849_1264735","RESULT":"1","MESSAGE":"查询成功，查到风险名单信息"}', 'BlackListCheck': '{"guid":"20180414152701_6RI2K7N8_1264742","RESULT":"1","MESSAGE":"命中黑名单"}'}
"""
"""
{'PaymentBlackVerify': '{"detail":{"resultCode":"2001","resultMsg":"未命中风险信息"},"guid":"20180414153132_49DURf66_1265093","RESULT":"2","MESSAGE":"查询成功，无数据"}', 'RiskListCombineInfo': '{"guid":"20180414153132_J92w93x2_1265131","RESULT":"2","MESSAGE":"查询无结果"}', 'BlackListCheck': '{"guid":"20180414153133_727adF8r_1264627","RESULT":"2","MESSAGE":"未命中黑名单"}'}
"""


