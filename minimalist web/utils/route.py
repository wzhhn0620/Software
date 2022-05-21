import os
import sys
import serial
import serial.tools.list_ports


algorithm = ''
space_limit = []
enter_point = []
end_point = []
grid_num = 0
grid_point = {}
link_act = {}
points_act = {}
act_dict = {
    '1': [1,0],
    '2': [-1,0],
    '3': [0,1],
    '4': [0,-1],
    '5': [0,3],
    '6': [0,-3]
}
position2endpoint_dict = {
    '1': [1,0],
    '2': [5,0],
    '3': [5,2],
    '4': [3,2],
    '5': [1,2],
    '6': [1,3],
    '7': [3,3],
    '8': [5,3],
    '9': [5,5],
    '10': [3,5],
    '11': [1,5],
}
pathList = []


def input_txt_resolve():
    global algorithm,space_limit,enter_point,end_point,grid_num     #声明使用全局变量
    module_dir = os.path.dirname(__file__)  # 获取当前目录
    file_path = os.path.join(module_dir, 'input.txt')
    f = open(file_path,'r')
    lines = f.readlines()
    f.close()
    algorithm = lines[0]
    space_limit = lines[1].strip('\n').split(' ')
    enter_point = list(map(int,lines[2].strip('\n').split(' ')))    #将数组中的字符串转为int
    # end_point = list(map(int,lines[3].strip('\n').split(' ')))
    end_point = [3,5]
    grid_num = lines[4].strip('\n')
    x = 1
    for i in lines[5:]:
        i_new = i.strip('\n').split(' ')
        i_num = list(map(int,i_new[:2]))
        link_act.update({ str(x) : i_new[2:]})
        grid_point.update({ str(x) : i_num })
        points_act.update({ str( i_num ) : str(x)})
        x = x + 1
    # print(link_act)
    # print(grid_point)



class handle_algorithm():
    def __init__(self, start_grid , end_grid , all_grid , act_grid , link_grid , num_grid , limit_grid ,output_text ,act_dict):
        self.start_grid = start_grid
        self.end_grid = end_grid
        self.all_grid = all_grid
        self.act_grid = act_grid
        self.link_grid = link_grid
        self.num_grid = num_grid
        self.limit_grid = limit_grid
        self.output_text = output_text
        self.act_dict = act_dict

    def BFS_alm(self):
        queue = []
        A_vertex = '0'
        queue.append(self.start_grid)
        seen = set()
        end_seen = set()
        A_start = self.link_grid[str(self.start_grid)]
        A_end = self.link_grid[str(self.end_grid)]
        seen.add(A_start)
        end_seen.add(A_end)
        parent = {A_start : None}  # 记录一下父子节点这样方便求最短路
        while (A_vertex != A_end):
            vertex = queue.pop(0)
            nodes = []
            A_vertex = self.link_grid[str(vertex)]
            link_vertex = self.act_grid[A_vertex]
            for i in link_vertex:
                act_vertex = self.act_dict[i]
                c = [vertex[i] + act_vertex[i] for i in range(len(vertex))]
                nodes.append(c)
            for w in nodes:
                A_w = self.link_grid[str(w)]
                if A_w not in seen:
                    queue.append(w)
                    seen.add(A_w)
                    parent[A_w] = A_vertex
            # print("当前出队的是：", vertex)
        re_start = A_end
        result = []
        motion_step = []
        while re_start:
            i_n = self.all_grid[re_start]
            result.append(i_n)
            re_start = parent[re_start]
            if re_start:
                i_l = self.all_grid[re_start]
                step = [i_n[i] - i_l[i] for i in range(len(i_l))]
                motion_step.append(step)
                # print(i_n,i_l)
            else:
                break
        result = result[::-1]
        motion_step = motion_step[::-1]
        motion_step_send = ""
        for i in motion_step:
            if i == [1,0]:
                motion_step_send += " 11"
            elif i == [-1,0]:
                motion_step_send += " 12"
            elif i == [0,1] or i == [0,3]:
                motion_step_send += " 13"
            else:
                motion_step_send += " 14"
        print(motion_step)
        return motion_step_send




def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def str2int(str):
    try:
        int(str)
        return int(str)
    except ValueError: #报类型错误，说明不是整型的
        try:
            float(str) #用这个来验证，是不是浮点字符串
            return int(float(str))
        except ValueError:  #如果报错，说明即不是浮点，也不是int字符串。   是一个真正的字符串
            return False

def toHex(num):
    """
    :type num: int
    :rtype: str
    """
    chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hexStr = ""

    if num < 0:
        num = num + 2 ** 32

    while num >= 16:
        digit = num % 16
        hexStr = chaDic.get(digit, str(digit)) + hexStr
        num //= 16
    hexStr = chaDic.get(num, str(num)) + hexStr

    return hexStr



class HC_05():
    def __init__(self):
        self.ser = serial.Serial()
        # self.port_check()

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.data_num_send = 0
        x_t = 0
        self.i_t = 0
        self.show_pic = 0
        self.data_count = 0
        self.CountStart1 = 0

    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        self.Com_list = []
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.Com_list.append(port[0])
        print(self.Com_list[1])
        if len(self.Com_Dict) == 0:
            print(" 无串口")
        return self.Com_list

        # 打开串口

    def port_open(self,com):
        print(com)
        self.ser.port = com
        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = "N"

        try:
            self.ser.open()
        except:
            return None
        return self.ser.isOpen()

    # 关闭串口
    def port_close(self):
        try:
            self.ser.close()
        except:
            pass
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.data_num_sended = 0


    # 发送数据
    def data_send(self,input_data):
        if self.ser.isOpen():
            # 数据帧
            input_s = input_data

            if input_s != "":
                # ascii发送
                input_s = (input_s + 'FF')

                # 简单的发送16进制字符
                # ser.write(b'\xFE\xFE\xFE')
                # 但是上面的方法不够优雅，需要自己添加\x，非常麻烦，于是使用下面这个方法
                input_s = bytes.fromhex(input_s)

                num = self.ser.write(input_s)
                self.data_num_send += num
        else:
            pass


    # 接收数据
    def data_receive(self):
        data_list = []
        data_str = b""
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            while True:
                if data == b'\r':
                    data = self.ser.read(num)
                    if data == b'\n':
                        break
                else:
                    data_list.append(data)
                    data_str = data_str + data
                    data = self.ser.read(num)

            # self.data_count = self.data_count+1
            # data = data[0:-2]
            # plot_data = str2int(data)
            print(data_str)
            if data_str == b'end':
                print('end')
            # if data == b'start':
            #     self.CountStart1 = 1
            #     print("start")
            #
            # num = len(data)

            # 统计接收字符的数量
            self.data_num_received += num
            return data_str
        else:
            return None






# 按间距中的绿色按钮以运行脚本。
# if __name__ == '__main__':
#     input_txt_resolve()
#     HA = handle_algorithm(enter_point , end_point , grid_point , link_act , points_act , grid_num , space_limit , 'FAIL' , act_dict)
#     motion_step_result = HA.BFS_alm()
#     print(motion_step_result)
#     BLE_1 = HC_05()
#     Uart_Com_List = BLE_1.port_check()
#     print(Uart_Com_List)
#     result = BLE_1.port_open(Uart_Com_List[1])
#     print(result)
#     input_data = motion_step_result
#     BLE_1.data_send(input_data)
#     re_data = BLE_1.data_receive()
#     while re_data != b"OK":
#         re_data = BLE_1.data_receive()
#     BLE_1.port_close()


