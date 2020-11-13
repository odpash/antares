import requests
import time
qiwi_token = '8110be1d8175bd4d00243634157087fc'
telephone = '79222662956'


def check_transaction(my_login, api_access_token, keyword, need_sum):
    #try:
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + api_access_token
        parameters = {'rows': 50}
        h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters).json()
        sp = []
        for i in h['data']:
            if i['type'] == 'IN' and str(keyword).lower() in str(i['comment']).lower() and float(i['sum']['amount']) >= float(need_sum):
                addr = keyword.split('_')[1]
                return '1', addr
        return '0', ''
   # except Exception:
     #   return '9', ''


def send_p2p(api_access_token, to_qw, comment, sum_p2p):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + qiwi_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"}, "comment":"'+comment+'","fields":{"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    postjson['comment'] = comment
    print('yeyyeyey')
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
    return res.json()

print(check_transaction('79521940783', '7e013ca9c29f9cef2761b25679b7c6d4', 'hbr1mt6_RU013742216', 385))