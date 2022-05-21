from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from datetime import datetime
from utils import sqlheper
from utils import route
import re
import time
import json
# Create your views here.

def users_login(request):
    if request.method=='GET':
        return render(request,'userslogin.html',{'msg':''})
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        print(request.POST)
        user_list = sqlheper.get_list('select name,pwd from users','dc_pg')
        if {'name':u,'pwd':p} in user_list:
            if u == "root":
                return redirect('r_mode_select/?token={}&user={}'.format(1646548181534756,u))
            else:
                return redirect('mode_select/?token={}&user={}'.format(1985684896595235756,u))
        # 这里使用了redirect跳转的方法
        else:
            return render(request, 'userslogin.html', {'msg': '登陆失败，用户名或密码错误'})


def mode_select(request):
    if request.method=='GET':
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1985684896595235756":
            return render(request,'mode_select.html', {'token': token,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})


def r_mode_select(request):
    if request.method=='GET':
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1646548181534756":
            return render(request,'r_mode_select.html', {'token': token,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})


def deposit(request):
    components_list = sqlheper.get_list("select c_id,name,position,floor from components", 'dc_pg')
    if request.method=='GET':
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1646548181534756" or token=="1985684896595235756":
            print(components_list[0]['name'])
            return render(request,'deposit.html', {'token': token, 'components_list':components_list,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})
    else:
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1646548181534756" or token=="1985684896595235756":
            deposit_component_list = {}
            action = request.GET.get('action')
            if action=="0":
                sl_component_id = request.POST.get('sl_component')
                deposit_component_list = sqlheper.get_list_one("select name,inventory,position,floor from components where c_id=%s", 'dc_pg',(sl_component_id))
                print(deposit_component_list)

            else:
                position_list = []
                new_component_name = request.POST.get('new_component')
                deposit_component_list['name'] = new_component_name
                deposit_component_list['inventory'] = 'enough'
                deposit_component_list['floor'] = '1'
                position_dict = sqlheper.get_list("select position from components",'dc_pg')
                for i in position_dict:
                    position_list.append(i['position'])
                new_position = sqlheper.position_distribute(position_list)
                deposit_component_list['position'] = new_position
                sqlheper.modify("insert components set name=%s,inventory='enough',position=%s,floor='1'",'dc_pg', (deposit_component_list['name'], deposit_component_list['position']))
            now_time = datetime.now()
            # sqlheper.modify("insert users_operation set users=%s,component=%s,operate='deposit',robot=1,time=%s,position=%s", 'dc_pg',(user_name,deposit_component_list['name'],
            #                                                                                                          now_time,deposit_component_list['position']))
            route.input_txt_resolve()
            endpoint = route.position2endpoint_dict[deposit_component_list['position']]
            HA = route.handle_algorithm(route.enter_point , endpoint , route.grid_point , route.link_act , route.points_act , route.grid_num , route.space_limit , 'FAIL' , route.act_dict)
            motion_step_result = HA.BFS_alm()
            print("Send-data:",motion_step_result)
            BLE_1 = route.HC_05()
            Uart_Com_List = BLE_1.port_check()
            print(Uart_Com_List)
            result = BLE_1.port_open(Uart_Com_List[1])
            # print(result)
            input_data = motion_step_result
            BLE_1.data_send(input_data)
            re_data = BLE_1.data_receive()
            while re_data != b"OK":
                re_data = BLE_1.data_receive()
            BLE_1.port_close()
            # time.sleep(20)

            return render(request, 'deposit.html', {'token': token,'components_list':components_list,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})


def takeout(request):
    components_list = sqlheper.get_list("select c_id,name,position,floor from components where inventory='enough'",'dc_pg')
    if request.method=='GET':
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1646548181534756" or token=="1985684896595235756":
            print(components_list[0]['name'])
            return render(request,'takeout.html', {'token': token, 'components_list':components_list,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})
    else:
        token = request.GET.get('token')
        user_name = request.GET.get('user')
        if token=="1646548181534756" or token=="1985684896595235756":
            sl_component_id = request.POST.get('sl_component')
            takeout_component_list = sqlheper.get_list_one(
                "select name,inventory,position,floor from components where c_id=%s", 'dc_pg', (sl_component_id))
            print(takeout_component_list)
            time.sleep(10)
            return render(request,'takeout.html', {'token': token,'components_list':components_list,'user':user_name})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})



def inquire(request):
    if request.method=='GET':
        token = request.GET.get('token')
        if token=="1646548181534756" or token=="1985684896595235756":
            users_components_list = sqlheper.get_list("select * from users_operation order by o_id desc", 'dc_pg')
            components_list = sqlheper.get_list("select * from components", 'dc_pg')
            return render(request,'inquire.html', {'token': token, 'users_components_list':users_components_list , 'components_list':components_list})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})


def administration(request):
    if request.method=='GET':
        token = request.GET.get('token')
        if token=="1646548181534756":
            users_list = sqlheper.get_list("select * from users where u_id != 1", 'dc_pg')
            root_list = sqlheper.get_list("select * from users where u_id = 1", 'dc_pg')
            components_list = sqlheper.get_list("select * from components", 'dc_pg')
            return render(request,'administration.html', {'token': token, 'users_list':users_list , 'components_list':components_list , 'root_list':root_list})
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})
    else:
        token = request.GET.get('token')
        action = request.GET.get('action')
        # print(action)
        if token=="1646548181534756":
            if action=="0":
                change_id = request.POST.get('change_id')
                change_name = request.POST.get('change_name')
                change_pwd = request.POST.get('change_pwd')
                ret = {'status': True, 'message': None}
                if len(change_name) > 0 and len(change_pwd) > 0:
                    try:
                        sqlheper.modify("update users set name=%s,pwd=%s where u_id=%s", 'dc_pg',
                                            (change_name, change_pwd, change_id))
                    except Exception as e:
                        ret['status'] = False
                        ret['message'] = str(e)
                    return HttpResponse(json.dumps(ret))
                else:
                    return HttpResponse('姓名密码不能为空')
            else:
                add_name = request.POST.get('add_name')
                add_pwd = request.POST.get('add_pwd')
                ret = {'status': True, 'message': None}
                if len(add_name) > 0 and len(add_pwd) > 0:
                    try:
                        sqlheper.modify("insert into users(name,pwd) values (%s,%s)", 'dc_pg', (add_name,add_pwd))
                    except Exception as e:
                        ret['status'] = False
                        ret['message'] = str(e)
                    return HttpResponse(json.dumps(ret))
                else:
                    return HttpResponse('姓名密码不能为空')
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})

def del_user(request):
    if request.method=='GET':
        token = request.GET.get('token')
        if token=="1646548181534756":
            del_id = request.GET.get("nid")
            sqlheper.modify("delete from users where u_id = %s", 'dc_pg', del_id)
            sqlheper.modify("alter table users AUTO_INCREMENT=0", 'dc_pg')
            return redirect('../?token=1646548181534756')
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})

def del_component(request):
    if request.method=='GET':
        token = request.GET.get('token')
        if token=="1646548181534756":
            del_id = request.GET.get("nid")
            sqlheper.modify("delete from components where c_id = %s", 'dc_pg', del_id)
            sqlheper.modify("alter table components AUTO_INCREMENT=0", 'dc_pg')
            return redirect('../?token=1646548181534756')
        else:
            return render(request, 'userslogin.html', {'msg': '浏览失败，请先登录'})

