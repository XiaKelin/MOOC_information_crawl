from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pymysql
import selenium.webdriver.support.ui as ui

# driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
# url = 'https://www.icourse163.org/home.htm?userId=1034056275#/home/course'
# driver.get(url)
# time.sleep(2)
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
#
# studytime=[]
#获取学习时长
# CumLearnTime=soup.find_all(lambda tag:tag.name=='span'and tag.get('class')==['f-thide'])
# studytime.append(CumLearnTime[1].string)
# print(studytime)

# CumLearnTime=soup.find_all('div', class_=re.compile('u-ui-time-cont'))
# for span in CumLearnTime:
#     studytime.append(span.string)
#
# #获取学习课程数目
# counuminfo=soup.find_all('span', class_=re.compile('u-st-course_span2'))
# print(counuminfo)
# str=counuminfo[0].string
# if len(str)>2:
#     num=int(str[3:])
# else:
#     num=0
#
# # 获取学习课程内容
# if num!=0:
#     couinfo=soup.find_all('span', class_=re.compile('f-thide u-cc-courseFunc_span33'))
#     temp=''
#     for i in range(len(couinfo)):
#         temp=temp+'《'+couinfo[i].string+'》'
#     print(temp)
#

tabelname = 'python语言程序设计评论者信息_copy'
db = pymysql.connect(host='localhost', user='root', passwd='123456', db='mooc', charset='utf8')
cur=db.cursor()
cur.execute("update %s set stu_cou_num = 5 where order_num = 1" % tabelname)
# cur.execute("update %s set studycourse = %s where order_num = %d"%(tabelname,'《数据库》',1))