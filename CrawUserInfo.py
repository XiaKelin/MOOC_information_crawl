from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pymysql
import selenium.webdriver.support.ui as ui

coursename='python语言程序设计'

#在数据库中建立表以方便爬取到一条就存进数据库
db = pymysql.connect(host='localhost', user='root', passwd='123456', db='mooc', charset='utf8')
cur = db.cursor()
try:
    cur.execute("select * from %s评论者信息" % coursename)
    results = cur.fetchall()
    ori_len = len(results)
    print('数据库中存在%s评论者信息表'%coursename)
except:
    # 建立新表
    sql = "create table %s评论者信息" % coursename + "(order_num int(4) not null,\
         userhref varchar(100) not null,\
         username varchar(50),\
         status varchar(100) not null,\
         certifinum int(4) not null,\
         excellent varchar(500),\
         qualify varchar(500),\
         primary key(order_num)\
         )"
    cur.execute(sql)
    db.commit()
    ori_len = 0
    print('已在mooc_course数据库中建立新表' + coursename+'评论者信息')


userhrefs,usernames,statuses,certifinums,excellents,qualifies=[],[],[],[],[],[]



#通过CrawComment已经得到了用户主页信息，因此只需要从数据库中拿到这个信息
db = pymysql.connect(host='localhost', user='root', passwd='123456', db='mooc', charset='utf8')
cur = db.cursor()
try:
    cur.execute("select userhref from %s" %coursename)
    results = cur.fetchall()
    n = len(results)
    temp=[]
    for i in range(n):
        temp.append(results[i][0])
    userhrefs=temp[ori_len:]

    cur.execute("select username from %s" % coursename)
    results=cur.fetchall()
    temp=[]
    for i in range(n):
        temp.append(results[i][0])
    usernames=temp[ori_len:]
except:
    print('找不到该表')

user_info=[userhrefs,usernames,statuses,certifinums,excellents,qualifies]

driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
for i in range(len(userhrefs)):
    n=0
    statu = 0
    url=userhrefs[i]
    driver.get(url)
    time.sleep(2)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')

    # 获取身份信息
    statusinfo = soup.find_all('div', class_=re.compile('u-ui-tag'))
    if len(statusinfo) != 0:
        for spans in statusinfo:
            for span in spans:
                statuses.append(span.string)
    else:
        tinfo = []
        statusinfo = soup.find_all('span', class_=re.compile('u-ti-name_span32'))
        for spans in statusinfo:
            for span in spans:
                tinfo.append(span.string)
        statuses.append(tinfo[-1])
        statu = 1

    # 获取证书数量
    if statu==0:
        certifinum=soup.find_all('span',class_=re.compile('u-st-cert_span6'))
        str=certifinum[0].string
        if len(str)>3:
            n=int(str[3:])
            certifinums.append(n)
        else :
            n=0
            certifinums.append(n)
    else:
        n=0
        certifinums.append(n)


    if n>0:
        #driver.implicitly_wait(3)
        time.sleep(1)


        # ele=driver.find_element_by_class_name('u-st-cert_span6')
        # #driver.implicitly_wait(10)
        # ele.click()  #点击证书

        wait = ui.WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.find_element_by_class_name('u-st-cert_span6'))
        driver.find_element_by_class_name('u-st-cert_span6').click()


        driver.implicitly_wait(3)
        xy=driver.find_element_by_class_name('u-certCardNav-func_span6')
        xy.click()   #点击优秀证书
        time.sleep(1)
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        exceinfo=soup.find_all('span', class_=re.compile('u-certCard-courseFunc_span17'))
        userexc=''
        for div in exceinfo:
            userexc=userexc+'《'+div.string+'》'
        if len(userexc)==0:
            excellents.append('null')
        else:
            excellents.append(userexc)
        driver.implicitly_wait(3)
        xz=driver.find_element_by_class_name('u-certCardNav-func_span9')
        xz.click()  #点击合格证书
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        qualifyinfo = soup.find_all('span',{'class': 'u-certCard-courseFunc_span17'})
        userqua =''
        for div in qualifyinfo:
            userqua=userqua+'《'+div.string+'》'
        if len(userqua)==0:
            qualifies.append('null')
        else:
            qualifies.append(userqua)
    else:
        excellents.append('null')
        qualifies.append('null')

    cur = db.cursor()
    # sql = "insert into %s评论者信息" % coursename + "(order_num,userhref,username,status,certifinum,excellent,qualify) VALUES ('%d','%s','%s','%s','%d','%s','%s')" % \
    #       (
    #           ori_len + i + 1, user_info[0][i], user_info[1][i], user_info[2][i], user_info[3][i], user_info[4][i],
    #           user_info[5][i])  # 执行数据库插入操作
    sql = "insert into %s评论者信息" % coursename + "(order_num,userhref,username,status,certifinum,excellent,qualify) VALUES ('%d','%s','%s','%s','%d','%s','%s')" % \
          (
              ori_len + i + 1, userhrefs[i], usernames[i], statuses[i], certifinums[i], excellents[i],
              qualifies[i])  # 执行数据库插入操作
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cur.execute(sql)
    except Exception as e:
        # 发生错误时回滚
        db.rollback()
        print('第%d条数据存入数据库失败！' + str(e) % (ori_len +i + 1))
    else:
        db.commit()  # 事务提交
        print('第%d条数据已存入数据库' % (ori_len +i + 1))


driver.quit()
db.close()










