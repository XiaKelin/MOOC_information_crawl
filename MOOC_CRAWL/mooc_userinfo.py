# 多线程爬取用户主页信息
import requests
import json
import pandas as pd
from queue import Queue
import threading
import csv


# 获取用户信息的类，继承自threading.Thread
class GetUserInfo(threading.Thread):
    headers = {
        'cookie': 'NTESSTUDYSI=250b9d2bf3ee4bca8cf182ad74a00366; EDUWEBDEVICE=9d7e3a17e36847c1a7269875d0486090; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1584757849; WM_NI=n6khf8cAOsqCOEtEEgyxs7xMvuttIyx3C6wjDpTojTV9BuduKtj6FQznS0RHu2w6W2UJJIuX4OrNJIld7h7dlAgpSfIDeI3fZOH5vY%2FNKMS0v63G57whlwkms16Qko0UaGU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed7f344b0be8eb0d072f6b88ba3d85a968a8bbbf55ba2e997d7e86fa69f9dabf52af0fea7c3b92aaeeaa589e534a19f8194f4498d9bbca6c86dbba8bdd8fb47b6abbc95cc73bced8dd7f66288b09c90e96096e78e96e77f89aca6d7c55bbab29dd1d144b7eeb9d7d63a979686aaf854f891beafc943b0bcf989b670b09fa991d26e8b9cabaab26e9a9188d6f553ed9285aed23cb6eafda8b83db5b8a498ea67b1effab2ea65f48bafa8d837e2a3; WM_TID=BZQYT8hV7YtEUAQBUAYvRfrI7OfeECZu; __yadk_uid=VYttAGx16Bfqqf2lBGTxsbKPGQX0ETHA; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1584757897',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    # 初始化函数
    def __init__(self, queue, gLock, writer, *args, **kwargs):
        super(GetUserInfo, self).__init__(*args, **kwargs)
        self.queue = queue
        self.gLock = gLock
        self.writer = writer

    # 获取用户普通信息
    def personal_data(self, id, user_dict):
        url = 'http://www.icourse163.org/web/j/memberBean.getMocMemberPersonalDtoById.rpc?csrfKey=250b9d2bf3ee4bca8cf182ad74a00366'
        member_data = {
            'memberId': id,
        }
        member_response = requests.post(url, data=member_data, headers=self.headers)  # 注意，这一步即将我们‘人’的信息传入请求中
        member_response.encoding = 'utf-8'
        s = json.loads(member_response.text)
        user_dict['memberId'] = s['result']['memberId']
        user_dict['schoolName'] = s['result']['schoolName']
        user_dict['nickName'] = s['result']['nickName']
        user_dict['department'] = s['result']['department']
        user_dict['memberType'] = s['result']['memberType']
        user_dict['highestDegree'] = s['result']['highestDegree']
        user_dict['jobName'] = s['result']['jobName']
        user_dict['description'] = s['result']['description']
        user_dict['isTeacher'] = s['result']['isTeacher']
        user_dict['followCount'] = s['result']['followCount']
        user_dict['followedCount'] = s['result']['followedCount']

    # 获取用户学习课程数、发帖数、证书数信息
    def learn_statistic(self, id, user_dict):
        url = 'http://www.icourse163.org/web/j/learnerCourseRpcBean.getPersonalLearningStatisticDto.rpc?csrfKey=250b9d2bf3ee4bca8cf182ad74a00366'
        course_data = {
            'uid': id,
        }
        course_response = requests.post(url, data=course_data, headers=self.headers)
        course_response.encoding = 'utf-8'
        s2 = json.loads(course_response.text)
        user_dict['learingCoursesCount'] = s2['result']['learingCoursesCount']
        user_dict['postsCounts'] = s2['result']['postsCounts']
        user_dict['certsCount'] = s2['result']['certsCount']

    # 获取用户学习时长等信息
    def activity_statistic(self, id, user_dict):
        url = 'http://www.icourse163.org/web/j/MocActivityScholarshipRpcBean.getActivityStatisticsByUser.rpc?csrfKey=250b9d2bf3ee4bca8cf182ad74a00366'
        activity_data = {
            'userId': id,
        }
        activity_response = requests.post(url, data=activity_data, headers=self.headers)  # 注意，这一步即将我们‘人’的信息传入请求中
        activity_response.encoding = 'utf-8'
        s1 = json.loads(activity_response.text)
        user_dict['postCount'] = s1['result']['statistics']['postCount']
        user_dict['replyCount'] = s1['result']['statistics']['replyCount']
        user_dict['commentCount'] = s1['result']['statistics']['commentCount']
        user_dict['voteCount'] = s1['result']['statistics']['voteCount']
        user_dict['learnLongTimeCount'] = s1['result']['statistics']['learnLongTimeCount']

    def run(self):
        # 线程源源不断地从队列中取出id，直达队列为空停止
        while True:
            if self.queue.empty():
                break

            user_dict = {}

            id = self.queue.get(block=False)

            try:
                self.personal_data(id, user_dict)
                self.learn_statistic(id, user_dict)
                self.activity_statistic(id, user_dict)
            except:
                print("%s 连接失败，准备进行下一轮爬取！！！" % threading.current_thread())
                self.queue.put(id, block=False)   # 连接失败，但id已取出，如果不把id放回队列中会导致获取的信息不完整
                continue

            self.gLock.acquire()  # 上锁
            self.writer.writerow(user_dict)
            self.gLock.release()  # 解锁
            print("%s 正在爬取并写入数据......" % threading.current_thread())


def main():
    coursename = '软件测试'

    # 建表
    header = ['memberId', 'schoolName', 'nickName', 'department', 'memberType',
              'highestDegree', 'jobName', 'description', 'isTeacher',
              'followCount', 'followedCount',
              'postCount', 'replyCount', 'commentCount',
              'voteCount', 'learnLongTimeCount', 'learingCoursesCount', 'postsCounts',
              'certsCount']
    fp = open('./user_info_data/%s.csv' % coursename, 'a', newline='', encoding='utf-8')
    writer = csv.DictWriter(fp, fieldnames=header)
    writer.writeheader()

    # 初始化队列，存放用户id
    queue = Queue(-1)  # maxsize小于或者等于0，队列大小没有限制

    # 创建一个锁
    gLock = threading.Lock()

    # 打开评论文件获取user_href
    comment_data = pd.read_csv('./comment_data/%s.csv' % coursename, engine='python', encoding='utf_8_sig')
    user_href = comment_data['user_href']

    # 遍历得到每一个用户的id, 并放进安全队列中
    for i in range(user_href.shape[0]):
        user_id = user_href[i].replace('//www.icourse163.org/home.htm?userId=', '')
        queue.put(user_id)

    # 创建5个线程
    for i in range(5):
        t = GetUserInfo(queue, gLock, writer)
        t.start()


if __name__ == '__main__':
    main()
