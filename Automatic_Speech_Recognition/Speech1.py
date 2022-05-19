# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:18:06 2020

@author: 16438
"""
from aip import AipSpeech
import wave
import requests
import re
import time
import base64
from pyaudio import PyAudio, paInt16
import webbrowser
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = "1.wav"
API_KEY = '2E3pdfNMWLCqrMVtG4LSfERg'
SECRET_KEY = 'LmPuDqBIOGOCDW4R0G2cORwnkWoQP0vG'

# 需要识别的文件
AUDIO_FILE = '1.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:];  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

CUID = '123456PYTHON';
# 采样率
RATE = 16000;  # 固定值

DEV_PID = 80001
ASR_URL = 'http://vop.baidu.com/pro_api'
SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里开通极速版

# 忽略scope检查，非常旧的应用可能没有
SCOPE = False

"""  TOKEN start """
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')
"""  TOKEN end """
    
def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()

#录音
def my_record():
    pa = PyAudio()
    #打开一个新的音频stream
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = [] #存放录音数据
    
    t = time.time()
    print('正在录音...')
     
    while time.time() < t + 5:  # 设置录音时间（秒）
    	#循环read，每次read 2000frames
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()

def recognition(FILEPATH):
    token = fetch_token()
    speech_data = []
    with open(FILEPATH, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    #测试自训练平台需要打开以下信息
    #params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID, 'lm_id' : LM_ID}
    params_query = urlencode(params);

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    url = ASR_URL + "?" + params_query

    # print post_data
    req = Request(ASR_URL + "?" + params_query, speech_data, headers)
    try:
        f = urlopen(req)
        result_str = f.read()
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    return re.split('\[|\]', result_str)[1]

def openbrowser(text):
    # maps = {
    #     '百度': ['百度', 'baidu'],
    #     '腾讯': ['腾讯', 'tengxun'],
    #     '网易': ['网易', 'wangyi']
        
    # }
    if '百度' in text :
        webbrowser.open_new_tab('https://www.baidu.com')
    elif '腾讯' in text :
        webbrowser.open_new_tab('https://www.qq.com')
    elif '毛泽东' in text :
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % '毛泽东')
    elif 'NBA' in text :
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % 'NBA')
    elif '嵌入式系统开发' in text :
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % '嵌入式系统开发')
    elif 'AI' in text :
        webbrowser.open_new_tab('https://ai.baidu.com/')
    else:
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % text)

flag = 'y'
while flag.lower() == 'y':
    my_record()
    result = recognition(FILEPATH)
    print(result)
    if type(result) == str:
        openbrowser(result.strip('，'))
    flag = input('Continue?(y/n):')


