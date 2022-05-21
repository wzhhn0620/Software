import pymysql




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

def position_distribute(exsit_position):
    empty_position = ["1","2","3","4","5","6","7","8","9","10","11"]
    for i in exsit_position:
        empty_position.remove(i)
    return empty_position[0]











