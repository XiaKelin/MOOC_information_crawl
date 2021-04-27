# -*- coding:utf-8 -*-
import requests
import re
import time
import csv

# MOOC中的讨论区主要分为三个部分，第一个是主题帖，第二个是主题帖的回复帖，第三个是回复帖的评论帖

# 三个请求头都会用到的公共部分
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    #'content-length': '333',
    'content-type': 'text/plain',
    'cookie': 'EDUWEBDEVICE=b11b80102e1447f992b43f731757921a; hasVolume=true; videoResolutionType=3; bpmns=1; __yadk_uid=ufvhB2nJOvQihehG9iQmSLLgT55Dw5f6; MOOC_PRIVACY_INFO_APPROVED=true; videoVolume=1.00; NTES_YD_PASSPORT=uZvgKkOsDgui69srLI0UsKNFeQnhXErlfwPJaReZQRDQsHBnse9N0v4lAq8errrXbizSOODWIdRe5hSAWI353ZdHpteS4qx3_sD6gC1yb26dqPK9PxVk7NKo1_HUaAHI5pDvPw9RcrMSsa_L1Lk0aB4_HZrzFZdkJ_R1hpw.5k0A80N4jmLlKAyRTs418MsIztDWX_HiZ77Y3dF6Oj80QNLqi; P_INFO=13871461352|1588212566|1|imooc|00&99|null&null&null#yun&530100#10#0#0|&0|null|13871461352; WM_TID=aWSkPY6P9TlBAQBRBFc7FBtTus3MtHQv; WM_NI=dMqihciOTyb9C4qrAFri11kbwgP0NPDnmPBlUJzIgh6H2CAXVyuRrwouwmm3UfO%2Br%2BuAoxjErkOfL4FMTyRvhIoBt6swb%2BWX%2BeVQH9pzyx40HwcI%2FXtH2cf9VDgz8L7DYTk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea5ef469697828ab862b8bc8ea7d15a938e8e85b54bb389fbb2d879a5bffab8b62af0fea7c3b92aa893bf8aeb69ab919c9ae13381ecbf93c44eb2b7ffd2ea6ab5b9a0d1cd5c88b2a3b1c1689796b6aae664f698fea4c45496a7bbb3f17dadabb98ef03997ba81ccf121b79fa199e94fb2b58187cf4086939c9ad17eac97a1a3f73eb1a9aeccd654e9bb9ab2cb33b4a6b799b73c8ca9adaaae54b898fe84e533969ca99bbb48f59c97b5ea37e2a3; NTESSTUDYSI=00b7cce637ee463fa719fdc837bc8dbb; STUDY_INFO="yd.69ca32d4f1254677b@163.com|8|1406029550|1588301100310"; STUDY_SESS="NkwFftYnxgQ47lb25Zfben8BjRAz8sdT9VrcYAD3D7TLbJPKkjUtMI+Vs2aE6gsK4zLoF9AVV5eMYYSsV4b9jt/8uwaxO0SDnHu9fKF9Lr/TSUudDn4Wx9M1LzGmpHIoA/ZH12MP/xtmMcCa7JO6NNo7d68vDZEdeP3tzPlYZw8Lhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_PERSIST="7nsHdihHmslMSGTX6QwtVzR+NtubTEOTUZWgfkYdeyQAR5soraGCZkk8SSVS4DS5MwT8H6g8+2NFuqyC35eZxEuw6qkWHlIxFZDEKLdVqXOkmd5DXm+5wTrsTmDVBL/k0Sa5Qch5bKJiFUTgDrZnXQBoPrDK4rg2RkXKTOJtka0C3pKaSIpXnn0j3ySePtsLDxhQt+2hbcGKT+V/3PRYZg7f1/DJzLRaGg6jfkld/nHZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1406029550#|#1573577685357; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1588141522,1588212418,1588224722,1588301104; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1588301119',
    'origin': 'https://www.icourse163.org',
    'referer': 'https://www.icourse163.org/learn/PKU-1207230807?tid=1207574207',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}


# 控制爬取整个讨论的流程和逻辑
def get_all_discussion():

    # 输入要爬取的课程的链接和课程名，注意需要在有讨论页下的链接
    url = 'https://www.icourse163.org/learn/PKU-1207230807?tid=1207574207#/learn/forumindex'
    # url = 'https://www.icourse163.org/learn/WHU-1207492805?tid=1207844202#/learn/forumindex'
    course_name = "QQQQQQQ"  # 输入你要爬取的课程名

    # 获取学校课程编号以及termId
    schoolCourse = re.findall('learn/(.*?)\?tid=',url)[0]   # schoolCourse = PKU-1207230807
    termId = re.findall('tid=(\d+)#', url)[0]  # termId = 1207574207

    # 改变headers的referer参数
    headers['referer'] = 'https://www.icourse163.org/learn/' + schoolCourse + '?tid=' + termId

    # 建表，用来存储爬取到的信息
    columns = ['type_label', 'post_id', 'reply_id', 'comment_id', 'subject', 'content', 'author_id',
               'author_nickName', 'public_time', 'follow_count', 'vote_count']
    fp = open('./%s_discussion.csv' % course_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(columns)

    # 初始设置主题帖的页数为1，通过is_end参数来控制主题帖的页数，从而避免先用selenium来得到主题帖的总页数
    pageIndex = 1
    while True:
        is_end = get_post(schoolCourse, termId, pageIndex, writer)
        if is_end:
            break
        else:
            print('第{}页主题写入完成!'.format(pageIndex))
            print('*'*50)
            pageIndex += 1


# 获取主题帖信息
def get_post(schoolCourse, termId, pageIndex,writer):
    url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getAllPostsPagination.dwr'
    data = {
        'callCount': 1,
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '7057dd407d3240c4a716838487e23437',
        'c0-scriptName': 'PostBean',
        'c0-methodName': 'getAllPostsPagination',
        'c0-id': 0,
        # 课程 id
        'c0-param0': 'number:' + termId,
        'c0-param1': 'string:',
        'c0-param2': 'number:1',
        # 当前页码
        'c0-param3': 'string:' + str(pageIndex),
        # 页码内容量
        'c0-param4': 'number:20',
        'c0-param5': 'boolean:false',
        'c0-param6': 'null:null',
        # 毫秒级时间戳
        'batchId': round(time.time() * 1000)
    }

    is_end = False
    try:
        # 如果不加timeout有可能会出现连接不成功的问题，详情参见https://blog.csdn.net/qq_39451578/article/details/104216121
        response = requests.post(url, data=data, headers=headers, timeout=(5, 10)).text
        # js 代码末尾信息分析，这里是找到返回信息的最后一行中的result，判断返回信息是否为空
        response_result = re.findall("results:(.*?)}", response)[0]

    except Exception:
        print('【主题帖post请求失败！！！】')
        return is_end   # 如果请求失败直接返回爬取下一页主题。

    if response_result == 'null':
        is_end = True
    else:
        try:
            object = re.findall('s(\d+)\.poster=s(\d+)', response)  # 找到这一页信息的所有post和poster对象
            for i in range(0, len(object)):
                post = 's' + object[i][0]  # post对象
                poster = 's' + object[i][1]  # poster对象

                # 帖子层面的信息
                typeLabel = '1'
                postId = re.findall(post + '\.id=(\d+)', response)[0]
                replyId = ''
                commentId = ''
                subject = re.findall(post + '\.title="(.*?)";', response)[0].encode().decode("unicode-escape")
                try:
                    # 注意，这个正则表达式里面有分号，如果不加分号某些内容将会出错
                    content = re.findall(post + '\.shortIntroduction="(.*?)";', response)[0].encode().decode("unicode-escape")
                except Exception:   # 有可能主题没有描述
                    content = ''
                publicTime = re.findall(post + '\.postTime=(\d+)', response)[0]
                followCount = re.findall(post + '\.countReply=(\d+)', response)[0]
                voteCount = re.findall(post + '\.countVote=(-?\d+)', response)[0]   # 注意，这里可能会有负数

                # 发帖人层面的信息
                authorId = re.findall(poster + '\.id=(\d+)', response)[0]
                authorName = re.findall(poster + '\.nickName="(.*?)"', response)[0].encode().decode("unicode-escape")

                info_list = [typeLabel, postId, replyId, commentId, subject, content,
                             authorId, authorName, publicTime, followCount, voteCount]

                writer.writerow(info_list)
                print("第{ %s }页 第 { %d } 条主题帖已存入" % (pageIndex, i+1))

                # 如果回帖数大于0，则继续爬取回帖信息
                followCount = int(followCount)
                if followCount > 0 :
                    # 初始设置回复帖的页数为1，通过reply_isEnd参数来控制主题帖的页数，从而避免先用selenium来得到主题帖的总页数
                    page_reply = 1
                    while True:
                        reply_isEnd = get_reply(postId, page_reply, writer=writer)
                        if reply_isEnd:
                            break
                        else:
                            print('    第{}页回复帖写入完成!'.format(page_reply))
                            page_reply += 1

        except Exception:
            print('主题写入错误！')

    return is_end


# 获取回复帖信息
def get_reply(postID, page_reply,writer):
    url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getPaginationReplys.dwr'
    data = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '00b7cce637ee463fa719fdc837bc8dbb',
        'c0-scriptName': 'PostBean',
        'c0-methodName': 'getPaginationReplys',
        'c0-id': '0',
        'c0-param0': 'number:' + postID,   # 帖子的id
        'c0-param1': 'number:2',
        'c0-param2': 'number:' + str(page_reply),   # 页数
        'batchId': round(time.time() * 1000)
    }

    reply_isEnd = False
    try:
        # 如果不加timeout有可能会出现连接不成功的问题，详情参见https://blog.csdn.net/qq_39451578/article/details/104216121
        response = requests.post(url, data=data, headers=headers, timeout=(5, 10)).text
        # js 代码末尾信息分析，这里是找到返回信息的最后一行中的result，判断返回信息是否为空这个方法不能用，所以判断返回的长度，如果小于200肯定为空
        response_result = len(response)
    except Exception:
        print('【回复帖post请求失败！！！】')
        return reply_isEnd

    if response_result <= 200:
        reply_isEnd = True
    else:
        try:
            object = re.findall('s(\d+)\.replyer=s(\d+)', response)
            for i in range(0, len(object)):
                reply = 's' + object[i][0]  # post对象
                replyer = 's' + object[i][1]  # poster对象

                # 帖子层面的信息
                typeLabel = '2'
                postId = postID
                replyId = re.findall(reply + '\.id=(\d+)', response)[0]
                commentId = ''
                subject = ''
                content = re.findall(reply + '\.content="(.*?)";', response)[0].encode().decode("unicode-escape")
                publicTime = re.findall(reply + '\.replyTime=(\d+)', response)[0]
                followCount = re.findall(reply + '\.countComment=(\d+)', response)[0]
                voteCount = re.findall(reply + '\.countVote=(-?\d+)', response)[0]  # 注意，这里可能会有负数

                # 发帖人层面的信息
                authorId = re.findall(replyer + '\.id=(\d+)', response)[0]
                authorName = re.findall(replyer + '\.nickName="(.*?)"', response)[0].encode().decode("unicode-escape")

                info_list = [typeLabel, postId, replyId, commentId, subject, content,
                             authorId, authorName, publicTime, followCount, voteCount]

                writer.writerow(info_list)
                print("    第 %d 条回复帖已存入" % (i + 1))

                # 如果评论数大于0，则继续爬取评论信息
                followCount = int(followCount)
                if followCount > 0:
                    get_comment(replyId,writer=writer)

        except Exception:
            print('回复帖写入错误！')

    return reply_isEnd


# 获取评论帖信息
def get_comment(replyID,writer):
    url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getPaginationComments.dwr'
    data = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '00b7cce637ee463fa719fdc837bc8dbb',
        'c0-scriptName': 'PostBean',
        'c0-methodName': 'getPaginationComments',
        'c0-id': '0',
        'c0-param0': 'number:' + replyID,  # 帖子的id
        'c0-param1': 'number:1',
        'batchId': round(time.time() * 1000)
    }

    try:
        response = requests.post(url, headers=headers, data=data).text
    except Exception:
        print("【评论帖post请求失败！！！】")
        return

    try:
        object = re.findall('s(\d+)\.commentor=s(\d+)', response)
        for i in range(0, len(object)):
            comment = 's' + object[i][0]  # comment对象
            commentor = 's' + object[i][1]  # commentor对象

            # 帖子层面的信息
            typeLabel = '3'
            postId = re.findall(comment + '\.postId=(\d+)', response)[0]
            replyId = replyID
            commentId = re.findall(comment + '\.id=(\d+)', response)[0]
            subject = ''
            content = re.findall(comment + '\.content="(.*?)";', response)[0].encode().decode("unicode-escape")
            publicTime = re.findall(comment + '\.commentTime=(\d+)', response)[0]
            followCount = ''
            voteCount = re.findall(comment + '\.countVote=(-?\d+)', response)[0]  # 注意，这里可能会有负数

            # 发帖人层面的信息
            authorId = re.findall(commentor + '\.id=(\d+)', response)[0]
            authorName = re.findall(commentor + '\.nickName="(.*?)"', response)[0].encode().decode("unicode-escape")

            info_list = [typeLabel, postId, replyId, commentId, subject, content,
                         authorId, authorName, publicTime, followCount, voteCount]

            writer.writerow(info_list)
            print("        第 %d 条评论帖已存入" % (i + 1))
    except Exception:
        print("评论帖写入错误！！！")


if __name__ == '__main__':
    # 记录程序花费的时间
    start_time = time.time()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))

    get_all_discussion()

    end_time = time.time()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    print('用时{}秒!'.format(end_time - start_time))

