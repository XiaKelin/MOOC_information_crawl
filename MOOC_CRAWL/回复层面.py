import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import time
import datetime
import pandas as pd
import numpy as np
# 读取post数据集，因为回复页面需要用到其中部分数据作为参数
post_df = pd.read_csv('./tiezi_test.csv')

base_url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getPaginationReplys.dwr' # 这里要换成对应Ajax请求中的链接

#从开发者选项上把request headers把参数拷贝下来
#再按正确格式更改~~
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '343',
    'content-type': 'text/plain',
    'cookie': 'NTESSTUDYSI=a6517bbd5c7949298df5ef20fa306fcb; EDUWEBDEVICE=ec89fae563bb454890c114b4bc1de49c; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1588216439; WM_NI=PepIQG9NichdBFTS%2F35ZeNQuH6xs0vTmueIxEHQNMzvTfBRK1Gu0ea9fH%2BSs1BbHNJlpvnezkAMawkBKy7bgP1Nzo7L28zT50niax%2FmNo1Gslcz7l3psZtMk8rJ7eZLKTTc%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea5d521889da8d7f07993eb8ab7d54b868b9bbbf85ff5989db6f67f8ab3f78cae2af0fea7c3b92a94bbc0aad44dfb92a784eb70829a9cb4ae39f786abafd47f8ceab894b37e98b3bb86cc7487989fafd072b68caaa3d141f399bbd1e86bfbba88ccd279f39eaea9cd42b0b0ba8fe872a99f8382f6618295b7d8e16d94ef829bee3d90eef89bd73ff4b2a782fb25af92a1d2c679b0bdb6d8ef39b4ad9695d061fcae86d8e85290959cb5e237e2a3; WM_TID=%2Fh14vo%2BwD4hBRURRRUcuA%2BTGVluMi9lq; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1588223016',
    'origin': 'https://www.icourse163.org',
    'referer': 'https://www.icourse163.org/learn/CAU-23004?tid=1002299017',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}


# 向页面发送请求
def get_page(pid,current_page):
    t = time.time()
    params = {
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':'a6517bbd5c7949298df5ef20fa306fcb',
        'c0-scriptName':'PostBean',
        'c0-methodName':'getPaginationReplys',
        'c0-id':0,
        'c0-param0':'number:'+str(pid),
        'c0-param1':'number:2',
        'c0-param2':'number:'+str(current_page),
        'batchId':int(round(t * 1000)) #当前时间毫秒级时间戳
    }
    response = requests.post(base_url,data=params,headers=headers)
    if response.status_code == 200:
        print(response)
        return response #返回格式为javascript




import re
import js2py
def filter_tags(htmlstr): #返回文本预处理，去除闲杂信息
    #去除url
    re_curl=re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
    re_curls=re.compile(r'https://[a-zA-Z0-9.?/&=:]*',re.S)
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    # re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s=re_curl.sub('',htmlstr)#去除url
    s=re_curls.sub('',s)#去除url
    s = re_cdata.sub('', s)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    # s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    return s

def reply_change(text):
    #转换编码，以及去除头尾不必要信息，仅保留javascript内容
    text=text.encode('utf-8').decode("unicode_escape").splitlines()[2:-2]
    for i in range(0,len(text)):
        text[i]=filter_tags(text[i])
    text="".join(text)
    return text


def get_reply_detail(text, index):
    reply_content = js2py.eval_js(text + index + '.content')  # 回复内容
    comment_cnt = js2py.eval_js(text + index + '.countComment')  # 回复的评论数
    vote_cnt = js2py.eval_js(text + index + '.countVote')  # 回复的评论数
    reply_uid = js2py.eval_js(text + index + '.replyerId')  # 回复者用户id
    timeStamp = js2py.eval_js(text + index + '.replyTime')  # 回复者用户id
    reply_time = time.strftime("%Y/%m/%d", time.localtime(timeStamp / 1000))
    return reply_content, comment_cnt, vote_cnt, reply_uid, reply_time


import math


def get_reply(pid, reply_num):  # 获取指定贴子下的回复情况
    page_num = math.ceil(reply_num / 15)  # 该帖子的回复页数，每一页最多有15条回复
    tmp = pd.DataFrame(columns=['pid', 'reply_content', 'comment_cnt', 'vote_cnt', 'reply_uid', 'reply_time'])
    for i in range(1, page_num + 1):
        reply_info = get_page(pid, i)
        reply_info = reply_info.text  # 获取该页的回复情况
        text = reply_change(reply_info)  # 转换编码，以及去除头尾不必要信息，仅保留javascript内容
        index = int(text[5:6])  # 变量的起始下标
        # 这里有一个很无语的bug，如果文本内容中含有双引号的话，会与变量属性外的双引号配对，从而导致异常符号出现，所以在此设置了异常判断
        try:
            user_num = js2py.eval_js(text + 's' + str(index) + '.length')  # 查看该页面作者个数
            for i in range(1, user_num + 1):
                index_name = 's' + str(index + i)
                reply_content, comment_cnt, vote_cnt, reply_uid, reply_time = get_reply_detail(text, index_name)
                tmp = tmp.append([{'pid': pid, 'reply_content': reply_content, 'comment_cnt': comment_cnt,
                                   'vote_cnt': vote_cnt, 'reply_uid': reply_uid, 'reply_time': reply_time}],
                                 ignore_index=True)
        except Exception:
            tmp = tmp.append([{'pid': pid, 'reply_content': '', 'comment_cnt': '',
                               'vote_cnt': '', 'reply_uid': '', 'reply_time': ''}], ignore_index=True)
            print('贴子：' + str(pid) + '的该页回复爬取失败！')
            pass
        continue

    return tmp


# 爬取数据
# 初始化一个df，用于存放爬取结果
reply_df = pd.DataFrame(columns=['pid', 'reply_content', 'comment_cnt', 'vote_cnt', 'reply_uid', 'reply_time'])
for i in range(0, post_df.shape[0]):
    if post_df['reply_num'][i] > 0:
        pid = post_df['pid'][i]
        reply_num = post_df['reply_num'][i]
        reply_df = reply_df.append(get_reply(pid, reply_num))
    else:
        reply_df = reply_df.append([{'pid': post_df['pid'][i], 'reply_content': '', 'comment_cnt': '',
                                     'vote_cnt': '', 'reply_uid': '', 'reply_time': ''}], ignore_index=True)

reply_df.to_csv('./huifu_test.csv', mode='a', header=True)  # 可按需导出文件

