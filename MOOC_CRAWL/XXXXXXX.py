# -*- coding: GBK -*-
import requests
import json
import pandas as pd
from pandas import DataFrame
import csv
import time

start_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))


comment_data = pd.read_csv('C:/软件/QQ/消息记录/644915034/FileRecv/心理学：我知无不言，它妙不可言-第六次课_discussion.csv', delimiter=",",
                           engine='python')  # delimiter = ','
comment_data.drop_duplicates('author_id', 'first', inplace=True)
comment_data = comment_data.reset_index(drop=True)
# from json import jsonpath #从jsonpath库中导入jsonpath方法
headers = {
    'cookie': 'EDUWEBDEVICE=9d7e3a17e36847c1a7269875d0486090; __yadk_uid=VYttAGx16Bfqqf2lBGTxsbKPGQX0ETHA; WM_TID=BZQYT8hV7YtEUAQBUAYvRfrI7OfeECZu; NTESSTUDYSI=a4f12d2fe2e946cba8f3a7a781abd8d0; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1586826248,1587178760,1587353139,1587949422; WM_NI=X4mob9XmVZXX1WRF5zTUyXK8n7sk2a7CB8w9d6EjHqMLIoIJr%2F9LIHc5mEGvutNTClgKmSPErDVInW8IOsIaa9cIEGQV1aLpPYlHtWM6pG0kAGBET7klvXlRYqpAshA3WWY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea5e46ff28da3b1d273aa9a8fa2d45f969f9bbaaa4af7af9ca9cd43bc94bf83f22af0fea7c3b92a9ceca390e1339cb39abbdb54f3899ea7b872988bb7b9ca34aee9bd8cb16bf59d8ed9f633a8ea8b8bcb7b8f948790cc42b2f1f7adcc44a1eba3a6c67eb7ac82b5c268a595a3b4d34fb29c9aaaed5dfc978194cc6ba3e7adaac84d938aff82cf7c9487a4a9f75d8feac0a8b36183998ea6d73da9b4bab9ef5a9bafc0a2f26483ed99b8dc37e2a3; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1587949434',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive'
}


columns = ['memberId', 'schoolName', 'nickName', 'department', 'memberType',
                               'highestDegree', 'jobName', 'description', 'isTeacher',
                               'followCount', 'followedCount',
                               'postCount', 'replyCount', 'commentCount',
                               'voteCount', 'learnLongTimeCount', 'learingCoursesCount', 'postsCounts', 'certsCount',
                               'learnedCourses', 'enrolCounts', 'courseSchool', 'CertRecord', 'type',
                               'issueTime']

fp = open('./all_data.csv', 'a+', newline='', encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(columns)

# user_data = DataFrame(columns)  # 建表

print(comment_data['author_id'].shape[0])

for i in range(4150, comment_data['author_id'].shape[0]):
    id = comment_data.loc[i, 'author_id']  # comment_data.loc[i,'user_url'].replace('www.icourse163.org/home.htm?userId=','')

    url = 'http://www.icourse163.org/web/j/memberBean.getMocMemberPersonalDtoById.rpc?csrfKey=a4f12d2fe2e946cba8f3a7a781abd8d0'
    url1 = 'http://www.icourse163.org/web/j/MocActivityScholarshipRpcBean.getActivityStatisticsByUser.rpc?csrfKey=a4f12d2fe2e946cba8f3a7a781abd8d0'
    url2 = 'http://www.icourse163.org/web/j/learnerCourseRpcBean.getPersonalLearningStatisticDto.rpc?csrfKey=a4f12d2fe2e946cba8f3a7a781abd8d0'
    url3 = 'http://www.icourse163.org/web/j/learnerCourseRpcBean.getOtherLearnedCoursePagination.rpc?csrfKey=a4f12d2fe2e946cba8f3a7a781abd8d0'
    certUrl = 'http://www.icourse163.org/web/j/mocCertQueryBean.getCertRecordByUid.rpc?csrfKey=f31e17f00f5b44b69120a1e8d83b238e'

    member_data = {
        'memberId': id,
    }
    activity_data = {
        'userId': id,
    }
    course_data = {
        'uid': id,
    }
    learn_course = {
        'uid': id,
        'pageIndex': 1,
        'pageSize': 32
    }
    cert_course = {
        'uid': id,
        'pageNo': 1,
        'pageSize': 40,
        'type': 0
    }
    member_response = requests.post(url, data=member_data, headers=headers)  # 注意，这一步即将我们‘人’的信息传入请求中
    member_response.encoding = 'utf-8'
    s = json.loads(member_response.text)
    #     print(s)
    if s['result'] is None:
        continue
    memberId = s['result']['memberId']
    schoolName = s['result']['schoolName']
    nickName = s['result']['nickName']
    department = s['result']['department']
    memberType = s['result']['memberType']
    highestDegree = s['result']['highestDegree']
    jobName = s['result']['jobName']
    description = s['result']['description']
    isTeacher = s['result']['isTeacher']
    followCount = s['result']['followCount']
    followedCount = s['result']['followedCount']

    activity_response = requests.post(url1, data=activity_data, headers=headers)  # 注意，这一步即将我们‘人’的信息传入请求中
    activity_response.encoding = 'utf-8'
    s1 = json.loads(activity_response.text)
    #     print(s1)
    #     print(s1['result']['statistics']['postCount'])
    postCount = s1['result']['statistics']['postCount']

    replyCount = s1['result']['statistics']['replyCount']
    commentCount = s1['result']['statistics']['commentCount']
    voteCount = s1['result']['statistics']['voteCount']
    learnLongTimeCount = s1['result']['statistics']['learnLongTimeCount']

    course_response = requests.post(url2, data=course_data, headers=headers)  # 注意，这一步即将我们‘人’的信息传入请求中
    course_response.encoding = 'utf-8'
    s2 = json.loads(course_response.text)
    learingCoursesCount = s2['result']['learingCoursesCount']
    postsCounts = s2['result']['postsCounts']
    certsCount = s2['result']['certsCount']
    learn_response = requests.post(url3, data=learn_course, headers=headers)  # 注意，这一步即将我们‘人’的信息传入请求中
    learn_response.encoding = 'utf-8'
    s3 = json.loads(learn_response.text)
    #     print(s3)
    tmp = ''
    for c in s3['result']['list']:
        tmp = tmp + c['courseName'] + '|'
    learnedCourses = tmp
    #     print(tmp)
    tmp1 = ''
    for c in s3['result']['list']:
        tmp1 = tmp1 + str(c['enrollCount']) + '|'
    enrolCounts = tmp1
    #     print(tmp1)
    tmp2 = ''
    for c in s3['result']['list']:
        tmp2 = tmp2 + c['schoolName'] + '|'
    courseSchool = tmp2
    #     print('http://www.icourse163.org/home.htm?userId='+str(id))
    headers1 = {
        'cookie': 'EDUWEBDEVICE=9d7e3a17e36847c1a7269875d0486090; __yadk_uid=VYttAGx16Bfqqf2lBGTxsbKPGQX0ETHA; NTESSTUDYSI=f31e17f00f5b44b69120a1e8d83b238e; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1587949422,1588059209,1588132527,1588920457; STUDY_SESS="IlchJo6oI9SgtfQim7GNIErKXXBIS3alel5wrHTarIoCsv5PFrJrKtQ6bC23MBzCkqInCL4sLAozhSoDVW9RYATD6odvaAmhdxJIOqWXDpU7dSkO/kKSyTGrvL8SJ7MqS31jjAhEzJTp2WqlUzas6B2E0SlmzKmd8xNHxDY6G/OwuMA5qor2rk1cYJzG53H7+P6MxCmnJEvne6pPMc9TTJJnThNrM7aj0X5LVpSBvjbLw5fdXCQwNyKM/WUn8cg8PZQg5CkSa71ZRqP7BEq6mzx3PbdW/lcrwvKcbNUJ6aZKlOh/Gwx6G1S/X4FQ7qd/8bGpyjihrpiYh5PNu6bTkwdL1Vafy6DH+RvVWHWrhGvoSNgBJvj6rpi+1ibQdijc"; STUDY_INFO=UID_244A53C71D7AD68A53C0F807CD72FDD2|4|1398444353|1588920472382; NETEASE_WDA_UID=1398444353#|#1567579367950; WM_NI=lgWjav4LmqmbP2os%2FZgscPO%2FrNGYw3OSjXy4svU%2FCmOsnUx0cmgSs2ihCZvKa4w3FNHW%2FSQwTXb5K0CF0iNguAh%2FnLKdanY2%2F6X76Sce94nF9Q2NN0vf669jKaYCm9bUdXQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee99b85982f0f7d1cc54f2bc8ea3d15a839f8fabf85ee9ad85b6e46090888794d12af0fea7c3b92ab0b9998be47ef894a392f06a94eea194ae52a5adadb1ce25b29289baf6398d8da6b9fc40b1aa9bd0c2678dada2b6fb3ca1b3a9b4f23aabb88dbbf541a3ecb9d4c5468c89e1b4d47d9888aed6ca3c819a008acd6db79fa8d0ed4889bcaf8fdc3aedea98d8b559a1bbf7d5ed4efb8ffeafcd3cb6bafad7bc6289bf97a4f033a28bacb9d437e2a3; WM_TID=BZQYT8hV7YtEUAQBUAYvRfrI7OfeECZu; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1588921656',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Referer': 'http://www.icourse163.org/home.htm?userId=' + str(id)
    }

    cert_response = requests.post(certUrl, data=cert_course, headers=headers1)  # 注意，这一步即将我们‘人’的信息传入请求中
    cert_response.encoding = 'utf-8'
    s4 = json.loads(cert_response.text)
    #     print(s4)
    tmp = ''
    for c in s4['result']['mocCertCardDtos']:
        tmp = tmp + c['courseName'] + '|'
    CertRecord = tmp
    #     print(tmp)
    tmp1 = ''
    for c in s4['result']['mocCertCardDtos']:
        tmp1 = tmp1 + str(c['type']) + '|'
    type = tmp1
    #     print(tmp1)
    tmp2 = ''
    for c in s4['result']['mocCertCardDtos']:
        tmp2 = tmp2 + str(c['issueTime']) + '|'
    issueTime = tmp2
    #     print(tmp2)
    #     if i%500 == 0:
    #         print('第%d条数据录入结束'%i)

    # 存入csv文件
    info_list = [memberId, schoolName, nickName, department, memberType,
                               highestDegree, jobName, description, isTeacher,
                               followCount, followedCount,
                               postCount, replyCount, commentCount,
                               voteCount, learnLongTimeCount, learingCoursesCount, postsCounts, certsCount,
                               learnedCourses, enrolCounts, courseSchool, CertRecord, type,
                               issueTime]
    writer.writerow(info_list)

    if i % 100 == 0:
        print('第%d条数据录入结束' % i)

end_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
print('用时{}秒!'.format(end_time - start_time))