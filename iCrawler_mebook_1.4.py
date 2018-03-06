# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7
#爬取“BTKitty”的磁力链接，并保存到exls文件中。
# 1.1版增加了对不提供链接的书籍的过滤功能。
# 1.4版完善了更新日期的提取


import requests
from bs4 import BeautifulSoup
import os
import re
import xlwt
import time
import datetime
ver=datetime.datetime.now().strftime('%Y-%m-%d')

print "本程序可以爬取“Meebook.cc”主页中的下载链接，并保存为excel文档。"
print "********************"
print

#使用workbook方法，创建一个新的工作簿
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
#添加一个sheet，名字为mysheet，参数overwrite就是说可不可以重复写入值，就是当单元格已经非空，你还要写入
sheet = book.add_sheet('BOOK',cell_overwrite_ok=True)
biaotoulist=["序号","书名","收录时间","下载页面","百度链接","验证码","主要内容"]
for k in range(7):
    sheet.write(0,k,list(biaotoulist)[k])
    book.save(u"我的小书屋"+str(ver)+".xls")


# 设置报头,Http协议,增加参数Refer对付防盗链设置
header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36','Referer': "http:://http://www.mzitu.com/"}
parser = 'html.parser'
j=1
pages=int(raw_input(u"请输入爬取页数："))
for i in range(pages):
    url = "http://mebook.cc/page/"+str(i+1)  # 爬取目标
    cur_page = requests.get(url, headers=header)
    soup = BeautifulSoup(cur_page.text, parser)
    bookLists=soup.find_all(attrs={'class':'content'})
    for bookList in bookLists:
        if u"公告" in bookList.text:
            k=1        
        else:
            k=1
            bookUrl=bookList.find_all('a')[k]
            bookUrl=bookUrl['href']
            bookPage=requests.get(bookUrl, headers=header)
            bookCont=BeautifulSoup(bookPage.text, parser)
            bookTitle=bookCont.find(attrs={'class':'sub'}).text
            bookIntro=bookCont.find(id="content").text
            bookTime=""
            if bookCont.find(attrs={'class':'downbtn'}):                
                downUrl=bookCont.find(attrs={'class':'downbtn'})
                downUrl=downUrl['href']
                baiduPage=requests.get(downUrl, headers=header)
                baiduCont=BeautifulSoup(baiduPage.text, parser)
                baiduUrl=baiduCont.find(attrs={'class':'list'}).find('a')
                baiduUrl=baiduUrl['href']
                baiduCode=baiduCont.find(attrs={'class':'desc'}).text
                bookTime=list(re.split(u'\n|',baiduCode))[5].replace(u"更新日期：","")
                baiduCode=list(re.split(u'\n|',baiduCode))[7]
                baiduCode=list(re.split(u'：|',baiduCode))[2].replace(u"天翼云盘密码","")
            else:
                downUrl='不提供下载'                
                baiduUrl='不提供下载'                
                baiduCode=""
            bookInfo=[str(j),bookTitle,bookTime,downUrl,baiduUrl,baiduCode,bookIntro]
            for l in range(7):
                sheet.write(j,l,list(bookInfo)[l])
            book.save(u"我的小书屋"+str(ver)+".xls")
            print ("第"+str(j)+'项纪录提取完成！')
            j=j+1            
    print ("&&& 第"+str(i+1)+"页提取完成！\n")
print "****************\n"
print ("共提取"+str(i+1)+"页，共提取"+str(j-1)+"项记录。")
           

        
    
   
