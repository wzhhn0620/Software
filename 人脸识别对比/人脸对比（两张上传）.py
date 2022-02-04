# encoding:utf-8
import requests
import json
import base64
import pygame
import time
import cv2 as cv
from aip import AipSpeech


api1 = 'xxx'

#语音模块初值
APP_ID = 'xxx'
API_KEY = 'xxx'
SECRET_KEY = 'xxx'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def find_face():
    capture = cv.VideoCapture(0)
    while (True):
        ret, frame = capture.read()
        frame = cv.flip(frame, 1)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        face_detector = cv.CascadeClassifier("haarcascade_frontalface_alt_tree.xml所在位置")
        faces = face_detector.detectMultiScale(gray, 2, 1)  # 第二个参数是移动距离，第三个参数是识别度，越大识别读越高
        if len(faces) > 0:
            for x, y, w, h in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 后两个参数，一个是颜色，一个是边框宽度
            cv.imwrite("out.jpg", gray)
        cv.imshow("result", frame)
        c = cv.waitKey(10)
        if c == 27:
            break

    cv.destroyAllWindows()


def get_token():
    response=requests.get(api1)
    access_token=eval(response.text)['access_token']
    api2="https://aip.baidubce.com/rest/2.0/face/v3/match"+"?access_token="+access_token
    return api2


def read_img(img1,img2):
    with open(img1,'rb') as f:
        pic1=base64.b64encode(f.read())
    with open(img2,'rb') as f:
        pic2=base64.b64encode(f.read())
    params=json.dumps([
        {"image":str(pic1,"utf-8"),"image_type":'BASE64',"face_type":"LIVE"},
        {"image":str(pic2,"utf-8"),"image_type":'BASE64',"face_type":"IDCARD"}
    ])
    return params


def analyse_img(file1,file2):
    params=read_img(file1,file2)
    api=get_token()
    content=requests.post(api,params).text
    print(content)
    score=eval(content)['result']['score']
    if score>80:
        print('你好,图片识别相似度度为'+str(score))
        words = '你好,图片识别相似度度为'+str(score)
    else:
        print('奇了怪了，朋友你是谁')
        words = '奇了怪了，朋友你是谁'

    result = client.synthesis(words, 'zh', 1, {
            "vol": 5,#音量
            "spd": 3,#音速
            "pit": 9,#语调
            "per": 1#0:女 1:男 3:逍遥 4:萝莉
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)

    file = r'audio.mp3'
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)

    pygame.mixer.music.play()
    time.sleep(5)
    pygame.mixer.music.stop()

find_face()
analyse_img("xxx.JPG","out.jpg")