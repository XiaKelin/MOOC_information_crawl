from selenium import webdriver
import re
from bs4 import BeautifulSoup
import pymysql

#executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
driver=webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
# url='https://www.icourse163.org/course/BIT-268001'  #Python语言程序设计
url='https://www.icourse163.org/course/ZJU-199001'   #程序设计入门——C语言
driver.get(url)
cont=driver.page_source

#获得初始页面代码，接下来进行简单的解析
soup=BeautifulSoup(cont,'html.parser')

#得到课程名称
coursenameinfo=soup.find_all('span',class_=re.compile('course-title f-ib f-vam'))
coursename=coursenameinfo[0].string


ele=driver.find_element_by_id("review-tag-button")  #模仿浏览器就行点击查看课程评价的功能
ele.click()
pagenum=0

try:
    xyy=driver.find_element_by_class_name("ux-pager_btn__next")#翻页功能，类名不能有空格，有空格可取后边的部分
except :
    print('该课程评论只有一页')
    pagenum=1


connt=driver.page_source
soup=BeautifulSoup(connt,'html.parser')

#得到评论页数
if pagenum !=1:
    pageinfo=soup.find_all('a',class_=re.compile('th-bk-main'))
    pagenum=int(pageinfo[-2].string)

acontent,aname,atime,acourse,asupport,astarnum,ahref=[],[],[],[],[],[],[]

if pagenum>1:
    for i in range(pagenum):
        xyy.click()
        connt = driver.page_source
        soup = BeautifulSoup(connt,'html.parser')
        content = soup.find_all('div',{'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})  # 包含全部评论项目的总表标签
        cname = soup.find_all('a', { 'class': 'primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'})
        ctime=soup.find_all('div',{'class':'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'})
        ccourse=soup.find_all('div',{'class':'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign'})
        csuppoprt = soup.find_all('span', {'class': 'primary-link'})
        cstarnum = soup.find_all('div', class_=re.compile('star-point'))
        chref = soup.find_all('a', class_=re.compile('primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'))

        for ctt in content:  # 第一页评论的爬取
            aspan = ctt.find_all('span')  # 刚获得一页中的content中每一项评论还有少量标签
            for span in aspan:
                acontent.append(span.string)  # 只要span标签里边的评论内容
        for names in cname:
            aname.append(names.string)
        for time in ctime:
            atime.append(time.string[3:])
        for course in ccourse:
            acourse.append(course.string)
        for csu in csuppoprt:
            sspan = csu.find_all('span', {'class': ''})
            for cspan in sspan:
                asupport.append(int(cspan.string))
        num = []
        for cst in cstarnum:
            cstt = []
            cstt = cst.find_all('i', class_=re.compile('star ux-icon-custom-rating-favorite'))
            num.append(len(cstt))
        for i in range(1, len(num)):
            astarnum.append(num[i])
        for href in chref:
            ahref.append('http:' + href.get('href'))
else:
        connt = driver.page_source
        soup = BeautifulSoup(connt, 'html.parser')
        content = soup.find_all('div',
                                {'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})  # 包含全部评论项目的总表标签
        cname = soup.find_all('a', {
            'class': 'primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'})
        ctime = soup.find_all('div', {'class': 'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'})
        ccourse = soup.find_all('div',
                                {'class': 'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign'})
        csuppoprt = soup.find_all('span', {'class': 'primary-link'})
        cstarnum = soup.find_all('div', class_=re.compile('star-point'))
        chref = soup.find_all('a', class_=re.compile(
            'primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'))

        for ctt in content:  # 第一页评论的爬取
            aspan = ctt.find_all('span')  # 刚获得一页中的content中每一项评论还有少量标签
            for span in aspan:
                acontent.append(span.string)  # 只要span标签里边的评论内容
        for names in cname:
            aname.append(names.string)
        for time in ctime:
            atime.append(time.string[3:])
        for course in ccourse:
            acourse.append(course.string)
        for csu in csuppoprt:
            sspan = csu.find_all('span', {'class': ''})
            for cspan in sspan:
                asupport.append(int(cspan.string))
        num = []
        for cst in cstarnum:
            cstt = []
            cstt = cst.find_all('i', class_=re.compile('star ux-icon-custom-rating-favorite'))
            num.append(len(cstt))
        for i in range(1, len(num)):
            astarnum.append(num[i])
        for href in chref:
            ahref.append('http:' + href.get('href'))


cm_info=[aname,acontent,atime,acourse,asupport,astarnum,ahref]

def save_comment(cm_info):
    db = pymysql.connect(host='localhost', user='root', passwd='123456', db='mooc', charset='utf8')
    cur = db.cursor()
    try:
        cur.execute("select * from %s" % coursename)
        results = cur.fetchall()
        ori_len = len(results)
    except:
        # 建立新表
        sql = "create table %s" % coursename + "(order_num int(4) not null,\
             username varchar(100) not null,\
             comment varchar(500),\
             pubtime varchar(20) not null,\
             pub_courtime varchar(10) not null,\
             supportnum int(4),\
             starnum tinyint(1),\
             userhref varchar(100) not null,\
             primary key(order_num)\
             )"
        cur.execute(sql)
        db.commit()
        ori_len = 1
        print('已在mooc_course数据库中建立新表' + coursename)
    for i in range(len(cm_info[0])):
        cur = db.cursor()
        # sql = "insert into %s"% subject+"(order_num,course,school,teacher,introduction,stu_num,start_time,link,id) VALUES ('%d','%s','%s','%s','%s','%d','%s','%s','%d')" %\
        #   (ori_len+i,kc_info[0][i],kc_info[1][i],kc_info[2][i],kc_info[3][i],kc_info[4][i],kc_info[5][i],kc_info[6][i],kc_info[7][i])#执行数据库插入操作
        sql = "insert into %s" % coursename + "(order_num,username,comment,pubtime,pub_courtime,supportnum,starnum,userhref) VALUES ('%d','%s','%s','%s','%s','%d','%d','%s')" % \
              (
              ori_len + i, cm_info[0][i], cm_info[1][i], cm_info[2][i], cm_info[3][i], cm_info[4][i], cm_info[5][i],
              cm_info[6][i])  # 执行数据库插入操作
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur.execute(sql)
        except Exception as e:
            # 发生错误时回滚
            db.rollback()
            print('第' + str(i + 1) + '条数据存入数据库失败！' + str(e))
        else:
            db.commit()  # 事务提交
            print('第' + str(i + 1) + '条数据已存入数据库')
    db.close()

save_comment(cm_info)

driver.quit()







