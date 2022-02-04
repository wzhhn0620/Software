from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import pymysql
from datetime import datetime
from utils import sqlheper
import re
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required

# Create your views here.

device_id_all = ['01','02','03','04','05','06','07','08','09','0a','0b']

def user_login(request):
    if request.method=='GET':
        request.session.flush()
        next_url = request.GET.get('next')
        print(next_url)
        return render(request,'login.html',{'msg':'','next_url':next_url})
    else:
        # print(request.url.sqlit('?',1)[1])
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        print(request.POST)
        time = datetime.now()
        p_user_list = sqlheper.get_list('select p_user,p_pwd from user_login','db1')
        robot__list = sqlheper.get_list('select robot_user,robot_pwd from robot_login', 'db1')
        if {'p_user':u,'p_pwd':p} in p_user_list:
            hash_token = sqlheper.hash_create(u,p,time)
            sqlheper.modify('update user_login set login_time=%s,token=%s where p_user=%s','db1',(time,hash_token,u))
            request.session["user"] = u
            request.session.set_expiry(60 * 60 * 24 * 14)  # 设置过期时间
            next_url = request.GET.get('next')
            if re.search('^/userlogin',str(next_url)):
                return redirect(next_url+'?token={}'.format(hash_token))
            else:
                return redirect('data_show/?token={}'.format(hash_token))
        # 这里使用了redirect跳转的方法
        elif {'robot_user':u,'robot_pwd':p} in robot__list:
            hash_token = sqlheper.hash_create(u,p,time)
            sqlheper.modify('update robot_login set login_time=%s,token=%s where robot_user=%s','db1',(time,hash_token,u))
            request.session["user"] = u
            request.session.set_expiry(60 * 60 * 24 * 14)  # 设置过期时间
            next_url = request.GET.get('next')
            if re.search('^/userlogin',str(next_url)):
                # return redirect(next_url)
                return redirect(next_url+'?token={}'.format(hash_token))
            else:
                return redirect('class/?token={}'.format(hash_token))
        else:
            hash_token = 0
            return render(request, 'login.html', {'msg': '登陆失败，用户名或密码错误','token':hash_token})

# @login_required
def data_show(request):
    ver_token = request.GET.get('token')
    user_token = sqlheper.get_list('select token from user_login', 'db1')
    if {'token':ver_token} in user_token:
        if request.method == 'GET':

            # robot1_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=1",'db1')
            # robot2_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=2", 'db1')
            # robot3_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=3", 'db1')
            # data_max = sqlheper.get_list("select max(id) from lora_data", 'db1')[0]['max(id)']
            # num_robot = sqlheper.get_list("select max(id) from robot_login", 'db1')[0]['max(id)']
            # robot_user = sqlheper.get_list("select robot_user from robot_login", 'db1')
            # robot1_data = sqlheper.dict2list(robot1_data)
            # robot2_data = sqlheper.dict2list(robot2_data)
            # robot3_data = sqlheper.dict2list(robot3_data)
            # robot_user = sqlheper.dict2list_robot_user(robot_user)
            #
            # if len(robot1_data[-1])>len(robot2_data[-1]):
            #     if len(robot1_data[-1])>len(robot3_data[-1]):
            #         pass
            #     else:
            #         robot1_data[-1] = robot3_data[-1]
            # elif len(robot2_data[-1])>len(robot3_data[-1]):
            #     robot1_data[-1] = robot2_data[-1]
            # else:
            #     robot1_data[-1] = robot3_data[-1]
            #
            # data_list = {
            #     'robot1':robot1_data,
            #     'robot2': robot2_data,
            #     'robot3': robot3_data,
            #     'data_max':data_max,
            #     'num_robot':num_robot,
            #     'robot_user':robot_user,
            # }

            data_list = {
                'token':ver_token
            }

            return render(request,'classes.html',data_list)
        else:
            time = request.POST.get('time')
            # time.strftime("%Y-%m-%d %H:%M:%S")
            robot_id = request.POST.get('robot_id')
            temp = request.POST.get('temp')
            humidity = request.POST.get('Humidity')
            lux = request.POST.get('Lux')
            # sqlheper.modify('insert ')
    else:
        return render(request, 'login.html', {'msg': '登陆失效，请重新登陆'})

# @login_required
def class_show(request):
    # ver_token = request.GET.get('token')
    # robot_token = sqlheper.get_list('select token from robot_login', 'db1')
    # if {'token':ver_token} in robot_token:
    #     class_list = sqlheper.get_list("select id,title from class", 'db1')
    #     return render(request,'classes.html',{'class_list':class_list})
    # else:
    #     return render(request, 'login.html', {'msg': '登陆失效，请重新登陆'})
    robot_data_all = {}
    robot_data_time = {}
    ver_token = request.GET.get('token')
    robot_id = request.GET.get('robotid')
    print("******************")
    print(robot_id)
    user_token = sqlheper.get_list('select token from user_login', 'db1')
    robot_token = sqlheper.get_list('select token from robot_login', 'db1')
    if {'token':ver_token} in robot_token:
        if request.method == 'GET':
            id = sqlheper.get_list('select id from robot_login where token=%s', 'db1',ver_token)

            for i in device_id_all:
                # print(i)
                robot_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where (robot_id = %s and device_id=%s)",'db1',(id[0]['id'],i))
                robot_data_time[i] = sqlheper.dict2list_onlytime(robot_data)
                robot_data = sqlheper.dict2list_withouttime(robot_data)
                robot_data_all["robot"+i] = robot_data

            time_lenmax = robot_data_time["01"]
            for i in device_id_all:
                if len(robot_data_time[i][1])>len(time_lenmax[1]):
                    time_lenmax = robot_data_time[i]


            print(robot_data_all)
            data_max = sqlheper.get_list("select count(id) from lora_data where robot_id=%s", 'db1', id[0]['id'])[0]['count(id)']
            num_robot = sqlheper.get_list("select max(id) from robot_login", 'db1')[0]['max(id)']

            # robot2_data = sqlheper.dict2list(robot2_data)
            # robot3_data = sqlheper.dict2list(robot3_data)
            data_list = robot_data_all
            data_list['xtime'] = time_lenmax
            data_list['data_max'] = data_max
            data_list['num_robot'] = num_robot
            data_list['robot_id'] = id[0]['id']
            return render(request,'class_index.html',data_list)
        else:
            time = request.POST.get('time')
            # time.strftime("%Y-%m-%d %H:%M:%S")
            robot_id = request.POST.get('robot_id')
            temp = request.POST.get('temp')
            humidity = request.POST.get('Humidity')
            lux = request.POST.get('Lux')
            # sqlheper.modify('insert ')
    elif {'token':ver_token} in user_token:
        if request.method == 'GET':
            id = eval(robot_id)
            for i in device_id_all:
                # print(i)
                robot_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where (robot_id = %s and device_id=%s)",'db1',(id,i))
                robot_data_time[i] = sqlheper.dict2list_onlytime(robot_data)
                robot_data = sqlheper.dict2list_withouttime(robot_data)
                robot_data_all["robot"+i] = robot_data
            time_lenmax = robot_data_time["01"]
            for i in device_id_all:
                if len(robot_data_time[i][1])>len(time_lenmax[1]):
                    time_lenmax = robot_data_time[i]
            data_max = sqlheper.get_list("select count(id) from lora_data where robot_id=%s", 'db1', id)[0]['count(id)']
            num_robot = sqlheper.get_list("select max(id) from robot_login", 'db1')[0]['max(id)']
            data_list = robot_data_all
            data_list['xtime'] = time_lenmax
            data_list['data_max'] = data_max
            data_list['num_robot'] = num_robot
            data_list['robot_id'] = id
            return render(request,'class_index.html',data_list)
    else:
        return render(request, 'login.html', {'msg': '登陆失效，请重新登陆'})

# @login_required
def add_class(request):
    ver_token = request.GET.get('token')
    robot_token = sqlheper.get_list('select token from robot_login', 'db1')
    if {'token':ver_token} in robot_token:
        if request.method=='POST':
            print(request.POST)
            time = request.POST.get('time')
            # time.strftime("%Y-%m-%d %H:%M:%S")
            robot_id = eval(request.POST.get('robot'))
            print(robot_id)
            temp = eval(request.POST.get('temp'))
            humidity = eval(request.POST.get('Humidity'))
            lux = eval(request.POST.get('Lux'))
            device_id = request.POST.get('device_id')
            sqlheper.modify("insert into lora_data(robot_id,temp,Humidity,Lux,time,device_id) values (%s,%s,%s,%s,%s,%s)", 'db1', (robot_id,temp,humidity,lux,time,device_id))
            return HttpResponse("update success")
    else:
        return HttpResponse("fail")

# @login_required
def download_class(request):
    ver_token = request.GET.get('token')
    robot_token = sqlheper.get_list('select token from robot_login', 'db1')
    if {'token':ver_token} in robot_token:
        robot_id = sqlheper.get_list('select id from robot_login where token=%s','db1',ver_token)
        data_id = sqlheper.get_list('select data_id from robot_download where robot_id=%s','db1',robot_id[0]['id'])
        data_all = sqlheper.get_list('select * from lora_data where id>%s','db1',data_id[0]['data_id'])
        max_data_id = sqlheper.get_list('select max(id) from lora_data','db1')
        sqlheper.modify('update robot_download set data_id=%s where robot_id=%s','db1',(max_data_id[0]['max(id)'],robot_id[0]['id']))
        if robot_id[0]['id']==max_data_id[0]['max(id)']:
            return HttpResponse('full')
        else:
            return JsonResponse(data_all,safe=False)
    else:
        return HttpResponse("fail")

# @login_required
def edit_class(request):
    robot_data_all = {}
    robot_data_time = {}
    if request.POST.get('pwd') == "123456789":
        id = request.POST.get('robot_id')
        # print(id)
        for i in device_id_all:
            robot_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where (robot_id = %s and device_id=%s)", 'db1',(id, i))
            robot_data_time[i] = sqlheper.dict2list_onlytime(robot_data)
            robot_data = sqlheper.dict2list_withouttime(robot_data)
            robot_data_all["robot" + i] = robot_data

        time_lenmax = robot_data_time["01"]
        for i in device_id_all:
            if len(robot_data_time[i][1]) > len(time_lenmax[1]):
                time_lenmax = robot_data_time[i]

        data_max = sqlheper.get_list("select count(id) from lora_data where robot_id=%s", 'db1',id)[0]['count(id)']
        num_robot = sqlheper.get_list("select max(id) from robot_login", 'db1')[0]['max(id)']
        # robot2_data = sqlheper.dict2list(robot2_data)
        # robot3_data = sqlheper.dict2list(robot3_data)
        data_list = robot_data_all
        data_list['xtime'] = time_lenmax
        print(time_lenmax[1])
        data_list['data_max'] = data_max
        data_list['num_robot'] = num_robot
        data_list['robot_id'] = id
        # data_list = {
        #     'robot_temp': robot_data[0],
        #     'robot_Humidity':robot_data[1],
        #     'robot_Lux':robot_data[2],
        #     'robot_t':robot_data[3],
        #     'data_max': data_max,
        #     'num_robot': num_robot,
        # }
        response = JsonResponse(data_list, safe=False)
        return response
    else:
        return render(request, 'login.html', {'msg': '非法请求'})



def edit_data(request):
    if request.POST.get('pwd')=="123456789":
    # print(id)
        robot1_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=1", 'db1')
        robot2_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=2", 'db1')
        robot3_data = sqlheper.get_list("select temp,Humidity,Lux,time from lora_data where robot_id=3", 'db1')
        data_max = sqlheper.get_list("select max(id) from lora_data", 'db1')[0]['max(id)']
        num_robot = sqlheper.get_list("select max(id) from robot_login", 'db1')[0]['max(id)']
        robot_user = sqlheper.get_list("select robot_user from robot_login", 'db1')
        robot1_data = sqlheper.dict2list(robot1_data)
        robot2_data = sqlheper.dict2list(robot2_data)
        robot3_data = sqlheper.dict2list(robot3_data)
        robot_user = sqlheper.dict2list_robot_user(robot_user)

        if len(robot1_data[-1]) > len(robot2_data[-1]):
            if len(robot1_data[-1]) > len(robot3_data[-1]):
                pass
            else:
                robot1_data[-1] = robot3_data[-1]
        elif len(robot2_data[-1]) > len(robot3_data[-1]):
            robot1_data[-1] = robot2_data[-1]
        else:
            robot1_data[-1] = robot3_data[-1]

        data_list = {
            'robot1_temp': robot1_data[0],
            'robot1_Humidity':robot1_data[1],
            'robot1_Lux':robot1_data[2],
            'robot2_temp': robot2_data[0],
            'robot2_Humidity': robot2_data[1],
            'robot2_Lux': robot2_data[2],
            'robot3_temp': robot3_data[0],
            'robot3_Humidity': robot3_data[1],
            'robot3_Lux': robot3_data[2],
            'robot_t':robot1_data[3],
            'data_max': data_max,
            'num_robot': num_robot,
            'robot_user':robot_user,
        }

        response = JsonResponse(data_list, safe=False)
        return response
    else:
        return render(request, 'login.html', {'msg': '非法请求'})
