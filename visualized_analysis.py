# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 12:42:05 2021

@author: 15209
"""

from pyecharts import Bar
from pyecharts import Line
from pyecharts import Pie
 #折线图,条形图，饼状图
from pyecharts import Page
from pyecharts import Grid

import pandas as pd
import re         #正则表达式



page1=Page("中国电影票房")
page2=Page("电影票房比较")
grid = Grid("电影票房比较",width=1000,height=800)


#读取excel表的数据
excel_file20 = '2020年票房排行榜.xls'
excel_file19 = '2019年票房排行榜.xls'
excel_file18 = '2018年票房排行榜.xls'
excel_file11 = '2011年票房排行榜.xls'
excel_file10 = '2010年票房排行榜.xls'

# file20 = pd.read_excel(excel_file20)
# file19 = pd.read_excel(excel_file19)
# file11 = pd.read_excel(excel_file11)
# file10 = pd.read_excel(excel_file10)

def to_list(file):

    files = pd.read_excel(file,usecols=[0,1,2,3,6]) #选取五列数据
    df_li = files.values.tolist()  #每一行为一个列表
    return df_li
   
    
        
def doline(filename):
    data_list = to_list(filename)
    ranks = []  #该年度排名
    Hranks = []   #电影总排名
    movie_names = [] #电影名称
    movie_boxs = []  #电影票房
    year = filename[0:4]  #通过excel命名前四个来表示年份
    for data in data_list[0:10]:   #选取前20个 
        ranks.append(data[0])
        Hranks.append(data[1])
        movie_names.append(data[2])
        # if '亿' in data[3]:
           # boxs = re.search(r"\d+\.?\d*" ,data[3]).group()#字符串，有单位
           # boxs = boxs*10000    #亿转成万
        # else:
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs.append(boxs)
       
       
    columns=['年度排名','历史排名','总票房']
    if year=='2020':
       line = Line("{}年电影".format(year),'票房单位万')      #用新版出现bug,老版本无法重构位置吗？
    else:
       line = Line("{}年电影".format(year),'票房单位亿')

    
    for i in range(10):
       datai = [ranks[i],Hranks[i],movie_boxs[i]]
       line.add(movie_names[i],columns,datai,is_lable_show=True)
     
    
        # 添加要展示的图表，并设置显示位置
   # grid.add(line, grid_bottom="60%", grid_right="60%")
    page1.add(line)    

def doBar():
    data_list1 = to_list(excel_file10)
    data_list2 = to_list(excel_file11)
    data_list3 = to_list(excel_file18)
    data_list4 = to_list(excel_file19)  #不比较2020 票房太差了 没有可比性

    # year1 = excel_file10[0:4]  #通过excel命名前四个来表示年份
    # year2 = excel_file11[0:4]  
    # year3 = excel_file18[0:4] 
    # year4 = excel_file19[0:4] 
    
    ranks1 = []  #该年度排名  data[0]
    ranks2 = [] 
    ranks3 = []
    ranks4 = [] 
    
    movie_names1 = [] #电影名称  data[2]
    movie_names2 = [] 
    movie_names3 = [] 
    movie_names4 = [] 
    
    movie_boxs1 = [] 
    movie_boxs2 = []  #电影票房   data[3]
    movie_boxs3 = []
    movie_boxs4 = [] 
    
    for data in data_list1[0:20]:   #选取前10个 
        ranks1.append(data[0])
        movie_names1.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs1.append(boxs)
        
    for data in data_list2[0:20]:   #选取前10个 
        ranks2.append(data[0])
        movie_names2.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs2.append(boxs)
   
    for data in data_list3[0:20]:
         ranks3.append(data[0])
         movie_names3.append(data[2])
         boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
         movie_boxs3.append(boxs)
    for data in data_list4[0:20]:
        ranks4.append(data[0])
        movie_names4.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs4.append(boxs)
          
       
   
    bar = Bar("电影年度比较","2010，2011，2018,2019,票房单位为亿")
    
    attrs1 = ["第{}".format(i+1) for i in range(20)]
    # attrs2 = ["11年-{}-{}".format(i+1,movie_names2[i]) for i in range(20)]
    # attrs3 = ["18年-{}-{}".format(i+1,movie_names3[i]) for i in range(20)]
    # attrs4 = ["19年-{}-{}".format(i+1,movie_names4[i]) for i in range(20)]
    
    
    v1 = [j for j in movie_boxs1[:20]]
    v2 = [j for j in movie_boxs2[:20]]
    v3 = [j for j in movie_boxs3[:20]]
    v4 = [j for j in movie_boxs4[:20]]
 
    bar.add('2010',attrs1,v1,is_label_show=True, is_datazoom_show=True)    #2010年
    bar.add('2011',attrs1,v2,is_label_show=True, is_datazoom_show=True)    #2011年
    bar.add('2018',attrs1,v3,is_label_show=True, is_datazoom_show=True)    #2018年
    bar.add('2019',attrs1,v4,is_label_show=True, is_datazoom_show=True)    #2019年
    
   
    grid.add(bar,grid_bottom="60%")
 
    # for i in range(5):
    #    datai = [ranks2[i],movie_boxs2[i]]
    #    bar.add(movie_names2[i],columns,datai,is_stack=True,mark_line=["min", "max"])    #2011年
       
    # grid.add(bar)
      
    # for i in range(5):
    #     datai = [ranks3[i],movie_boxs3[i]]
    #     bar.add(movie_names3[i],columns,datai,is_stack=True,mark_line=["min", "max"])    #2018年
    # grid.add(bar)   
    
    # for i in range(5):
    #     datai = [ranks4[i],movie_boxs4[i]]
    #     bar.add(movie_names4[i],columns,datai,is_stack=True,mark_line=["min", "max"])    #2019年
    # grid.add(bar)
        

def doall_line():
    data_list1 = to_list(excel_file10)
    data_list2 = to_list(excel_file11)
    data_list3 = to_list(excel_file18)
    data_list4 = to_list(excel_file19)  #不比较2020 票房太差了 没有可比性
    
    ranks1 = []  #该年度排名  data[0]
    ranks2 = [] 
    ranks3 = []
    ranks4 = [] 
    
    movie_names1 = [] #电影名称  data[2]
    movie_names2 = [] 
    movie_names3 = [] 
    movie_names4 = [] 
    
    movie_boxs1 = [] 
    movie_boxs2 = []  #电影票房   data[3]
    movie_boxs3 = []
    movie_boxs4 = [] 
    
    for data in data_list1[0:20]:   #选取前10个 
        ranks1.append(data[0])
        movie_names1.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs1.append(boxs)
        
    for data in data_list2[0:20]:   #选取前10个 
        ranks2.append(data[0])
        movie_names2.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs2.append(boxs)
   
    for data in data_list3[0:20]:
         ranks3.append(data[0])
         movie_names3.append(data[2])
         boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
         movie_boxs3.append(boxs)
    for data in data_list4[0:20]:
        ranks4.append(data[0])
        movie_names4.append(data[2])
        boxs = re.search(r"\d+\.?\d*" ,data[3]).group()   
        movie_boxs4.append(boxs)
          
       
   
    line = Line("电影年度比较","2010，2011，2018,2019")
    
    attrs1 = ["10年-{}-{}".format(i+1,movie_names2[i]) for i in range(20)]
    attrs2 = ["11年-{}-{}".format(i+1,movie_names2[i]) for i in range(20)]
    attrs3 = ["18年-{}-{}".format(i+1,movie_names3[i]) for i in range(20)]
    attrs4 = ["19年-{}-{}".format(i+1,movie_names4[i]) for i in range(20)]
    
    #如何给点命名！！散点图
    v1 = [j for j in movie_boxs1[:20]]
    v2 = [j for j in movie_boxs2[:20]]
    v3 = [j for j in movie_boxs3[:20]]
    v4 = [j for j in movie_boxs4[:20]]
 
    line.add('2010',attrs1,v1, mark_point=["average"])    #2010年
    line.add('2011',attrs2,v2,is_smooth=True)    #2011年
    line.add('2018',attrs3,v3,is_smooth=True)    #2018年
    line.add('2019',attrs4,v4,mark_point=["average"], mark_line=["max", "min"])    #2019年
    
    grid.add(line,grid_top="60%")
   
    
def main():
    #顺序表示折线图
    doline(excel_file20)
    doline(excel_file19)
    doline(excel_file11)
    doline(excel_file10)
    page1.render("movie.html")  
    
    doBar()
    #page2.render("compare.html")
    doall_line()
    grid.render("compare.html")
    
    

if __name__ == '__main__':
    main()





