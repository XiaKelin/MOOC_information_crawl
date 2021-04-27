from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options
import time
import csv


def get_comment(url, course_name, path):
    # 定义一个列表存放评论信息
    all_comment_list = []

    # 打开浏览器
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path=path)
    driver.get(url)

    # 找到“课程详情”按钮，并点击
    xyy = driver.find_element_by_id('review-tag-button')
    xyy.click()

    # 解析网页
    html = driver.page_source
    re_comment = re.compile('<!--[^>]*-->')
    result_content = re_comment.sub('', html)  # 去掉html中的注释
    soup = BeautifulSoup(result_content, 'html.parser')

    # 获取评论的页数
    pages = 0
    for li in soup.find_all('li', class_='ux-pager_itm'):
        pages = int(li.find('a').string)

    # 循环遍历获取每一页的数据
    x = 1
    while x <= pages:

        list_item_bodys = soup.find_all(class_='ux-mooc-comment-course-comment_comment-list_item_body')  # 找到每一个评论信息主体

        for list_item_body in list_item_bodys:
            # 获取主页链接
            user_href = list_item_body.find(
                class_='primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name').get('href')
            # 获取用户昵称
            user_name = list_item_body.find('a').text
            # 获取用户评分
            star_point = 0
            star_point_info = list_item_body.find_all(class_='ux-icon-custom-rating-favorite')
            for i in star_point_info:
                star_point += 1
            # 获取用户评论
            comment_info = list_item_body.find(class_='ux-mooc-comment-course-comment_comment-list_item_body_content')
            comment = comment_info.find('span').string
            # 获取发表评论的时间
            public_time = list_item_body.find(
                class_='ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time').text[3:]
            # 获取发表评论时的开课时间
            term_sign = list_item_body.find(class_='ux-mooc-comment-course-comment_comment-list_item_body_comment'
                                                   '-info_term-sign').text
            # 获取获赞数
            support_info = list_item_body.find('span', class_='primary-link')
            support = support_info.find('span', class_='').string

            # 把每个用户的评论信息放在一个字典中
            comment_dict = {
                'user_href': user_href,
                'user_name': user_name,
                'star_point': star_point,
                'comment': comment,
                'public_time': public_time,
                'term_sign': term_sign,
                'support': support
            }

            # 把每个用户的评论信息添加到总的列表中去
            all_comment_list.append(comment_dict)
            # page_list.append(comment_dict)

        # 翻页
        xyy = driver.find_element_by_class_name("ux-pager_btn__next")
        driver.implicitly_wait(2)
        xyy.click()
        time.sleep(1)  # 设置等待时间是为了正常获取页面，不然会出现第一页重复爬取的情况，但代价是爬取速度变慢
        html = driver.page_source
        re_comment = re.compile('<!--[^>]*-->')
        result_content = re_comment.sub('', html)  # 去掉html中的注释
        soup = BeautifulSoup(result_content, 'html.parser')
        x += 1

    print("已爬取了 %d 条评论！" % len(all_comment_list))

    # 将评论信息存储为json
    # with open('./comment_data/%s_all_comment.json' % course_name, 'w', encoding='utf-8') as fp:
    #     json.dump(all_comment_list, fp=fp, ensure_ascii=False, indent=4)   # indent是缩进，一般为2或者4

    # 将评论信息存储为csv文件
    header = ['user_href', 'user_name', 'star_point', 'comment', 'public_time', 'term_sign', 'support']
    with open('./comment_data/%s.csv' % course_name, 'w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=header)
        writer.writeheader()
        for i in range(len(all_comment_list)):
            writer.writerow(all_comment_list[i])


def main():
    start = time.time()
    course_url = 'https://www.icourse163.org/course/NWPU-1003591005'
    course_name = '软件测试'
    path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
    get_comment(course_url, course_name, path)
    end = time.time()
    print("该程序运行了 %s 秒" % (end-start))


if __name__ == '__main__':
    main()
