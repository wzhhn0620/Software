# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:35:48 2020

@author: 16438
"""

import requests
import re
import wordcloud
import jieba
import PIL .Image as image
import numpy as np

name=[]

def gethtmltext(url):
	try:
		headers = {'cookie':'xxx',
		'User-Agent':'xxx'}
		r=requests.get(url,headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return""

def parsePage(ilt,html):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            ilt.append([price,title])
            name.append(title)
    except:
        print("")
	
def printGoodsList(ilt):
    tpit="{:4}\t{:8}\t{:20}"
    print(tpit.format("序号","价格","名称"))
    count=0
    for g in ilt:
        count=count+1
        print(tpit.format(count,g[0],g[1]))
        
def create_wordcloud(name):
    mask = np.array(image.open("1.png"))
    # f = open("target.txt","r")
    # t = f.read()
    # f.close()
    ls = jieba.lcut(name)
    txt = " ".join(ls)
    
    w = wordcloud.WordCloud( font_path = "msyh.ttc",mask = mask,
    	width=1000,height=700,background_color="black",)
    w.generate(txt)
    w.to_file("result.png")
	
def main():
    goods='人工智能'
    depth=7
    start_url='https://s.taobao.com/search?initiative_id=staobaoz_20200211&q='+goods
    infoList=[]  
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=gethtmltext(url)
            parsePage(infoList,html)
        except:
            continue
    # printGoodsList(infoList)
    a="".join(name)
    create_wordcloud(a)
	
main()