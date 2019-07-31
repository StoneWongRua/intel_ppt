import urllib
import urllib.parse
import urllib.request
import base64
import json

client_id = 'PtGR84MlaNQL6KLPeB73A4Xd'
client_secret = 'Ze0KrGXEtyLykKAMbAn09xRWIfXsTjmc'


def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


#filename:图片名（本地存储包括路径）
def currency(filename):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/currency"
    

    f = open(filename, 'rb')
    img = base64.b64encode(f.read())
    
    params = dict()
    params['image'] = img
    params['show'] = 'true'
    params = urllib.parse.urlencode(params).encode("utf-8")
    #params = json.dumps(params).encode('utf-8')
    
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        #print(content)
        content=content.decode('utf-8')
        #print(content)
        data = json.loads(content)
        #print(data)
        result=data['result']
        print ('货币名称:',result['currencyName'])
        print ('货币代码:',result['currencyCode'])
        print ('货币年份:',result['year'])
        print ('货币面值:',result['currencyDenomination'])
    return result['currencyCode'],float(result['currencyDenomination']),result['year']

import re

def get_currency_rate(fromcurrency,tocurrency):
    fp = urllib.request.urlopen('http://webforex.hermes.hexun.com/forex/quotelist?code=FOREX'+fromcurrency+tocurrency+',&column=code,LastClose,UpdownRate&callback=ongetjsonpforex&_=1451543515359')
    html = fp.read().decode("utf-8")
    #print(html)
    fp.close()
    s = re.findall("\((.*)\)",str(html))[0]
    sjson = json.loads(s)
    rate = sjson["Data"][0][0][1]/10000
    #print (rate)
    return rate



def currency_value(filename):
    code,value,year=currency(filename)

    if code=='PEN':
        if year<='1991年':
            print ('已经作废不可兑换,谨防诈骗！')
            return
    if code=='DEI':
        print ('已经作废不可兑换,谨防诈骗！')
        return
    
    rate=get_currency_rate(code,'CNY')
    result=round(value*rate,3)
    print ('汇率（昨收盘）：',rate)
    print ('对应人民币（昨收盘）：',result)
    return result
    


import cv2

cap = cv2.VideoCapture(0)
index = 0
imgname = 0
    # 用循环不断获取当前帧 处理后显示出来
while True:
    index = index + 1
    #   捕获当前帧
    ret,img = cap.read()
    #    显示图像
    cv2.imshow('video',img)
    #   每5秒保存一张截图
    if index == 10:
        imgname = imgname + 1
        if imgname >= 5:
            imgname = 0
#           文件名字符串拼接
        fname = 'money.jpg'
#           写入截图
        cv2.imwrite(fname, img)
        print(fname + ' saved')
        img = fname
        currency_value(img)
        index = 0
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()











