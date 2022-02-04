import pymysql
import hashlib
from datetime import datetime

def get_list(sql,db_name,*args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db=db_name, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,*args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_list_one(sql,db_name,*args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db=db_name, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,*args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def modify(sql,db_name,*args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db=db_name, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,*args)
    conn.commit()
    cursor.close()
    conn.close()

def hash_create(u,p,time):
    data = "{}|{}|{}".format(time, u, p)
    hash_pwd = hashlib.sha1(data.encode('utf-8'))
    hash_pwd.update('黄安冉傻逼'.encode('utf-8'))
    return hash_pwd.hexdigest()

def dict2list(data_list):
    temp = []
    hum = []
    lux = []
    time = []
    j = 0
    for i in data_list:
        temp.append(i['temp'])
        hum.append(i['Humidity'])
        lux.append(i['Lux'])
        time.append(j)
        j = j+1
    list=[temp,hum,lux,time]
    return list

def dict2list_robot_user(data_list):
    result = []
    for i in data_list:
        result.append(i['robot_user'])
    return result

def dict2list_time(data_list):
    temp = []
    hum = []
    lux = []
    time = []
    j = 0
    for i in data_list:
        temp.append(i['temp'])
        hum.append(i['Humidity'])
        lux.append(i['Lux'])
        time.append((i['time'].strftime("%m-%d")+":{}").format(j))
        j = j+1
    list=[temp,hum,lux,time]
    return list

def dict2list_withouttime(data_list):
    temp = []
    hum = []
    lux = []
    for i in data_list:
        temp.append(i['temp'])
        hum.append(i['Humidity'])
        lux.append(i['Lux'])
    list=[temp,hum,lux]
    return list

def dict2list_onlytime(data_list):
    time1 = []
    time2 = []
    j = 0
    for i in data_list:
        time1.append((i['time'].strftime("%m-%d")+":{}").format(j))
        time2.append(j)
        j = j+1
    list=[time1,time2]
    return list