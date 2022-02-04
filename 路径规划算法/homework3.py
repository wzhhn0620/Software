import os


algorithm = ''
space_limit = []
enter_point = []
end_point = []
grid_num = 0
grid_point = {}
link_act = {}
points_act = {}
act_dict = {
    '1': [1,0,0],
    '2': [-1,0,0],
    '3': [0,1,0],
    '4': [0,-1,0],
    '5': [0,0,1],
    '6': [0,0,-1],
    '7': [1,1,0],
    '8': [1,-1,0],
    '9': [-1,1,0],
    '10': [-1,-1,0],
    '11': [1,0,1],
    '12': [1,0,-1],
    '13': [-1,0,1],
    '14': [-1,0,-1],
    '15': [0,1,1],
    '16': [0,1,-1],
    '17': [0,-1,1],
    '18': [0,-1,-1]
}
pathList = []


def input_txt_resolve():
    global algorithm,space_limit,enter_point,end_point,grid_num     #声明使用全局变量
    f = open('input.txt','r')
    lines = f.readlines()
    f.close()
    algorithm = lines[0]
    space_limit = lines[1].strip('\n').split(' ')
    enter_point = list(map(int,lines[2].strip('\n').split(' ')))    #将数组中的字符串转为int
    end_point = list(map(int,lines[3].strip('\n').split(' ')))
    grid_num = lines[4].strip('\n')
    x = 1
    for i in lines[5:]:
        i_new = i.strip('\n').split(' ')
        i_num = list(map(int,i_new[:3]))
        link_act.update({ str(x) : i_new[3:]})
        grid_point.update({ str(x) : i_num })
        points_act.update({ str( i_num ) : str(x)})
        x = x + 1
    print(link_act)
    print(grid_point)


class AStar_Point():
    """docstring for point"""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class AStar_Node():
    def __init__(self, point, g=0, h=0):
        self.point = point  # 自己的坐标
        self.father = None  # 父节点
        self.g = g  # g值
        self.h = h  # h值

    """
    估价公式：曼哈顿算法
     """

    def manhattan(self, endNode):
        self.h = (abs(endNode.point.x - self.point.x) + abs(endNode.point.y - self.point.y) + abs(endNode.point.z - self.point.z)) * 10

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

    def nodeinOpenList(self, OpenList):
        for nodeTmp in OpenList:
            if nodeTmp.point.x == self.point.x and nodeTmp.point.y == self.point.y \
                and nodeTmp.point.z == self.point.z:
                return True
        return False

    def nodeinCloseList(self, CloseList):
        for nodeTmp in CloseList:
            if nodeTmp.point.x == self.point.x and nodeTmp.point.y == self.point.y \
                and nodeTmp.point.z == self.point.z:
                return True
        return False

    def getNodeFromOpenList(self,OpenList):
        for nodeTmp in OpenList:
            if nodeTmp.point.x == self.point.x \
                and nodeTmp.point.y == self.point.y \
                    and nodeTmp.point.z == self.point.z:
                return nodeTmp
        return None



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
            print("当前出队的是：", vertex)
        print(parent)
        re_start = A_end
        result = []
        while re_start:
            result.append(self.all_grid[re_start])
            re_start = parent[re_start]
        result = result[::-1]
        print(result)
        self.re_output()


    def UCS_alm(self):
        pass

    def AStar_alm(self):
        openList = []
        closeList = []
        global pathList
        StartPoint = AStar_Point(self.start_grid[0], self.start_grid[1], self.start_grid[2])
        EndPoint = AStar_Point(self.end_grid[0], self.end_grid[1], self.end_grid[2])
        StartNode = AStar_Node(StartPoint)
        EndNode = AStar_Node(EndPoint)
        openList.append(StartNode)
        StartNode.manhattan(EndNode)
        while(1):
            nodeTemp = openList[0]
            for n in openList:
                if((n.g + n.h)<(nodeTemp.g + nodeTemp.h)):
                    nodeTemp = n
            CurrentNode = nodeTemp
            closeList.append(CurrentNode)
            openList.remove(CurrentNode)
            A_Current = self.link_grid[str([CurrentNode.point.x, CurrentNode.point.y, CurrentNode.point.z])]
            link_Current = self.act_grid[A_Current]
            for i in link_Current:
                act_Current = self.act_dict[i]
                c = [CurrentNode.point.x + act_Current[0], CurrentNode.point.y + act_Current[1], CurrentNode.point.z + act_Current[2]]
                c_point = AStar_Point(c[0], c[1], c[2])
                c_node = AStar_Node(c_point)
                if(c_node.nodeinCloseList(closeList)):
                    continue
                if(eval(i)>6):
                    gTemp = 14
                else:
                    gTemp = 10
                if(c_node.nodeinOpenList(openList) == False):
                    c_node.setG(gTemp)
                    c_node.manhattan(EndNode)
                    openList.append(c_node)
                    c_node.setFather(CurrentNode)
                else:
                    # 要从openList中将其取出来，因为需要其g值与h值
                    c_node = c_node.getNodeFromOpenList(openList)
                    if(CurrentNode.g + gTemp < c_node.g):
                        c_node.setG(CurrentNode.g + gTemp)
                        c_node.setFather(CurrentNode)

                print(gTemp)
            for nodeTmp in openList:
                if nodeTmp.point.x == EndNode.point.x \
                    and nodeTmp.point.y == EndNode.point.y \
                        and nodeTmp.point.z == EndNode.point.z :
                    nodeTmp = nodeTmp.getNodeFromOpenList(openList)
                    while True:
                        pathList.append(nodeTmp)
                        if nodeTmp.father != None:
                            nodeTmp = nodeTmp.father
                        else:
                            return True
            if len(openList) == 0:
                return False







    def re_output(self):
        f = open('output.txt','w')
        f.write(self.output_text)
        f.close()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    input_txt_resolve()
    HA = handle_algorithm(enter_point , end_point , grid_point , link_act , points_act , grid_num , space_limit , 'FAIL' , act_dict)
    HA.BFS_alm()
    result = HA.AStar_alm()
    if result:
        for i in pathList:
            print(i.point.x,i.point.y,i.point.z)

