

import os
import requests
import cv2
import base64
import json
from pprint import pprint
import time
class AnimalRecognizer(object):
    def __init__(self, api_key, secret_key):
        self.access_token = self._get_access_token(api_key=api_key, secret_key=secret_key)
        self.API_URL = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal' + '?access_token=' \
                       + self.access_token
    @staticmethod
    def _get_access_token(api_key, secret_key):
        api = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
              '&client_id={}&client_secret={}'.format(api_key, secret_key)
        rp = requests.post(api)
        if rp.ok:
            rp_json = rp.json()
            print(rp_json['access_token'])
            return rp_json['access_token']
        else:
            print('=> Error in get access token!')
    def get_result(self, params):
        rp = requests.post(self.API_URL, data=params)
        if rp.ok:
            print('=> Success! got result: ')
            rp_json = rp.json()
            pprint(rp_json)
            return rp_json
        else:
            print('=> Error! token invalid or network error!')
            print(rp.content)
            return None
    def detect(self, img_path):
        f = open(img_path, 'rb')
        img_str = base64.b64encode(f.read())
        params = {'image': img_str, 'with_face': 1}
        tic = time.clock()
        rp_json = self.get_result(params)
        toc = time.clock()
        print('=> Cost time: ', toc - tic)
        result = rp_json['result']
        print(result)


import cv2
if __name__ == '__main__':
    recognizer = AnimalRecognizer(api_key='PtGR84MlaNQL6KLPeB73A4Xd', secret_key='Ze0KrGXEtyLykKAMbAn09xRWIfXsTjmc')
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
            fname = 'flower.jpg'
#           写入截图
            cv2.imwrite(fname, img)
            print(fname + ' saved')
            img = fname
            recognizer.detect(img)
            index = 0
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
