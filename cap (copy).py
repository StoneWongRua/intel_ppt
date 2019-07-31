import numpy as np
import cv2

# 初始化摄像头
# cap = cv2.VideoCapture(0)

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
    if index == 100:
        imgname = imgname + 1
        if imgname >= 50:
            imgname = 0
#           文件名字符串拼接
        fname = str(imgname) + '.jpg'
#           写入截图
        cv2.imwrite(fname, img)
        print(fname + ' saved')
        index = 0
#   结束帧捕获的条件
#   等待50ms 即帧频为20fps
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
# 释放资源
cap.release()
cv2.destroyAllWindows()
