from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup

executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

url_head = 'https://www.icourse163.org/learn/CAU-23004?tid=1002299017#/learn/forumindex'
driver.get(url_head)
print("成功进入讨论区")

def get_panel_list():
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    time.sleep(5)
    panel_list=soup.find('div',class_ = 'j-panels').find_all('a',class_='tit')
    return panel_list


# 获取该板块下指定页的贴子信息
import re


def get_comment_detail(comment_list):
    # 初始化一个dataframe，用于暂存爬取结果
    df = pd.DataFrame(columns=["pid", "watch_num", "reply_num", "vote_num",
                               "post_title", "post_content", "post_uid", "post_time"])
    for comment in comment_list:
        comment_href = comment.find('a', class_='j-link').get('href')
        pid = re.search('(\d+)', comment_href).group()  # 贴子id，str
        watch_num = int(comment.find('p', class_='watch').text[3:])  # 贴子的浏览数
        reply_num = int(comment.find('p', class_='reply').text[3:])  # 贴子的回复数
        vote_num = int(comment.find('p', class_='vote').text[3:])  # 贴子的投票数

        reply_link = url_head.split('#')[0] + comment_href  # 进入贴子详情界面的连接
        reply_driver = webdriver.Chrome(executable_path=executable_path)
        reply_driver.get(reply_link)
        time.sleep(5)
        reply_soup = BeautifulSoup(reply_driver.page_source, 'html.parser')

        # 帖子题目+描述
        post = reply_soup.find('div', class_='j-post')
        post_title = post.find('h3', class_='j-title').text  # 贴子主题
        post_content = post.find('div', class_='j-content').text  # 贴子具体内容

        # 发帖信息，需要注意有些用户是匿名发表，此处需要进行一个判断
        post_info = post.find('div', class_='j-infoBox')
        if post_info.find('span', class_='userInfo').get('style') is None:
            post_uid = post_info.find('a', class_='f-fcgreen').get('href')
            post_uid = re.search('(\d+)', post_uid).group()  # 发帖者uid，str
        else:
            post_uid = '匿名发表'
        print(post_uid)
        post_time = post_info.find('div', class_='j-time').text  # 发帖时间

        # 把这一个贴子的信息存入df
        df = df.append([{"pid": pid, "watch_num": watch_num, "reply_num": reply_num, "vote_num": vote_num,
                         "post_title": post_title, "post_content": post_content, "post_uid": post_uid,
                         "post_time": post_time}], ignore_index=True)

        reply_driver.quit()  # 记得关闭
    return df


# 获取该板块下指定页的贴子列表
def get_comment(panel):
    df = pd.DataFrame(columns=["pid", "watch_num", "reply_num", "vote_num",
                               "post_title", "post_content", "post_uid", "post_time"])
    page_num = 0  # 初始化每个板块的页数
    panel_name = panel.text  # 每个板块的名字
    print('板块名称：' + panel_name)
    panel_url = url_head.split('#')[0] + panel.get('href')
    panel_driver = webdriver.Chrome(executable_path=executable_path)
    panel_driver.get(panel_url)
    time.sleep(5)
    panel_soup = BeautifulSoup(panel_driver.page_source, 'html.parser')
    pages = panel_driver.find_elements_by_class_name('zpgi')
    for i in range(0, len(pages)):
        if pages[i].text:
            page_num = pages[i].text
        else:
            break
    print('该板块下的主题页数为：' + page_num)
    for i in range(0, int(page_num)):
        comment_url = panel_url + '&p=' + str(i + 1)
        panel_driver.get(comment_url)
        time.sleep(5)
        panel_soup = BeautifulSoup(panel_driver.page_source, 'html.parser')
        comment_list = panel_soup.find(class_='j-data-list').find_all('li', class_='u-forumli')  # 获取贴子列表
        df = df.append(get_comment_detail(comment_list))  # 调用上述函数
    panel_driver.quit()
    df = df.reset_index(drop=True)
    return df


panel_list=get_panel_list()
df = get_comment(panel_list[2])  # 综合讨论区为第3个板块，将爬取结果存在df中
df.to_csv('./tiezi_test.csv', mode='a', header=True)  # 可按需导出文件
