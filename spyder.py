# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

1.BeautifulSoup4将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,

2.对于该网站信息，设置了登录验证，所以需要用到cookie信息登录，设置请求头
"""

import  requests
from bs4 import BeautifulSoup  #处理html数据的库
import xlwt

base_url = "http://58921.com"
year_url = "http://58921.com/alltime/"   #后面变动的是年份

headers = {
   # Cookie 登录验证
  "Cookie":"Hm_lvt_e71d0b417f75981e161a94970becbb1b=1623585188,1623585225,1623585266,1623596664; Hm_lpvt_e71d0b417f75981e161a94970becbb1b=1623598151; time=MTEzNTI2LjIxNjM0Mi4xMDI4MTYuMTA3MTAwLjExMTM4NC4yMDc3NzQuMTE5OTUyLjExMTM4NC4xMDQ5NTguMTE1NjY4LjEwNzEwMC4xMDkyNDIuMTEzNTI2LjEyMjA5NC4xMTk5NTIuMTA0OTU4LjExOTk1Mi4xMDcxMDAuMA%3D%3D; DIDA642a4585eb3d6e32fdaa37b44468fb6c=cv2800gehusdkfppi0trf062o0; remember=MTEzNTI2LjIxNjM0Mi4xMDI4MTYuMTA3MTAwLjExMTM4NC4yMDc3NzQuMTE5OTUyLjExMTM4NC4xMDQ5NTguMA%3D%3D",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}

def get_html(url,encoding):
    response = requests.get(url,headers=headers) 
    if response.status_code == 200:   #200：请求正常，服务器正常的返回数据。
        response.encoding = encoding   #将网页请求返回的结果按照网页的编码来（此网页是utf-8编码）
        return response.text
    else:
        return None


def year_list(url):
    """网页源代码访问 'http://58921.com/alltime/2019?page=1' 网页的第二页
       该函数功能为：得到改年份的所有电影。
    """
   
    year = url.split("/alltime/")[1]  #此处表示2019，指分割得到第二个为年份
    year_list = []
    
    
    # 获取页数
    html = get_html(url,encoding="utf-8")         #注意！！！！！！这里不写中文会乱码！！！
    soup = BeautifulSoup(html, "html.parser")     #html解码器
    item_list = soup.find("div",class_="item-list") 
    #注意！！class_下划线 不然会报错。div作为标记头，class作为标记，表示网页下面表示页数的整体代码，
    #每页代码为列表元素
    
    if item_list is not None:  
        pager_number = item_list.find("li", class_="pager_count").find("span",class_="pager_number").get_text()
        #因为网页页码处，总记录和页次，有相同的头标span,class，所以选择逐层找到
        page = int(pager_number.split("/")[1])  #表示总页数 2/27 代指27
    else:
        page = 1
    
    f=open("电影票房.csv","a",encoding='utf-8')
    for i in range(0,page):
        page_url = '{}?page={}'.format(url,i)    #翻页网址，搜索该年份所有电影
       # print(page_url)
        
        html = get_html(page_url,encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        content = soup.find("div",class_="table-responsive") #主体内容
        
        if content is not None:
            trs =content.table.tbody.find_all("tr")  #每一行数据存于trs列表
            for tr in trs:
                movie_info = []
                tcs = tr.find_all("td")         #电影的每列属性
                for index,tc in enumerate(tcs): #用于将一个可遍历的列表tds，同时列出数据下标和数据
                    # print(td)
                    if index == 3:      #第四列，票房是图片链接！
                        movie_info.append(tc.img['src'])
                    
                    else:
                        movie_info.append(tc.get_text())
                f.write(",".join(movie_info).strip())
                f.write("\n")
                year_list.append(movie_info)
        else:
            print("无该页数据")
    f.close()        
    print(year_list)
    save_to_excel("./{}年票房排行榜.xls".format(year),year_list)
    
 #网上学的
def save_to_excel(savepath,datalist):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('票房排行榜', cell_overwrite_ok=True)  # 创建工作表
    col = ("年度排名", "历史排名", "电影名称", "总票房", "总人次", "总场次","上映年份","操作")
    for i in range(0,8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, len(datalist)):
        print("第{}条".format(i + 1))
        data = datalist[i]
        if len(data) >= 8:# 数据完整才保存
            for j in range(0, 8):
                sheet.write(i + 1, j, data[j])
    book.save(savepath)  # 保存



def url_list():
    """拼接url"""
    return [year_url+str(i) for i in range(2018,2021)]

def main():
    for url in url_list():
       year_list(url)
       

if __name__ == '__main__':
    main()





