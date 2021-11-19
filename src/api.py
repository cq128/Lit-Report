# coding: utf-8
import json
import random
import requests
from hashlib import sha256

from user import User


def checkLogin(func):
    """检查用户登录状态
    ~~~
    在调用需要登录凭证的方法时，检查用户是否已经调用登录方法，如果没有，则调用登录方法
    """

    def wrapper(self):
        if self.user.token == "" or self.loginMsg == "":
            self.login()
        func(self)
    return wrapper


class UserAPI:
    """用户方法类
    """

    def __init__(self, user: User) -> None:
        """用户方法
        ~~~
        提供了一些可供学生调用的一般方法，包括登录、查看上报记录、上报等
        :param: user: 用户类，包括用户的账号（学号）、密码和登录凭证（可为空，通过登录获取）
        """
        self.user = user
        userAgents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
        ]
        self.userAgent = random.choice(userAgents)
        self.loginMsg = ""
        self.lastMsg = ""

    def login(self):
        """登录
        ~~~
        登录获取登录凭证，几乎所有的方法都离不开登录凭证
        """
        login_url = "http://hmgr.sec.lit.edu.cn/wms/healthyLogin"
        headers = {
            'Connection': "keep-alive",
            'Content-Type': "application/json;charset=UTF-8;Access-Control-Allow-Headers",
            'User-Agent': self.userAgent
        }
        data = {
            'cardNo': self.user.username,
            'password': sha256(self.user.password.encode('utf-8')).hexdigest()
        }
        response = requests.post(
            login_url, headers=headers, data=json.dumps(data), timeout=5)
        response_json = response.json()
        if response_json['code'] == 4002:
            raise Exception("密码错误")
        elif response_json['code'] == 4001:
            raise Exception("账号不存在")
        elif response_json['code'] == 200:
            self.user.token = response_json['data']['token']
            self.loginMsg = response_json['data']
            return True
        else:
            raise Exception("登录失败，未知错误")

    @checkLogin
    def getLast(self):
        """获取上报信息
        ~~~
        获取最近一次上报的信息，用以作为本次上报的基础
        """
        last_url = f"http://hmgr.sec.lit.edu.cn/wms/lastHealthyRecord?teamId={self.loginMsg['teamId']}&userId={self.loginMsg['userId']}"
        headers = {
            'token': self.user.token,
            'User-Agent': self.userAgent
        }
        response = requests.get(last_url, headers=headers, timeout=5)
        response_json = response.json()
        if response_json['code'] == 401:
            raise Exception("登录凭证不合法，请先调用上报方法检查错误")
        elif response_json['code'] == 200:
            self.lastMsg = response_json['data']
            return True
        else:
            raise Exception("获取上报信息失败，未知错误")

    @checkLogin
    def firstReport(self):
        """第一次上报方法
        ~~~
        利用登录获取的信息和最近上报的信息进行第一次上报
        """
        if self.lastMsg == "":
            try:
                self.getLast()
            except Exception as e:
                print(e)
        first_url = "http://hmgr.sec.lit.edu.cn/wms/addHealthyRecord"
        headers = {
            'Connection': "keep-alive",
            'Content-Type': "application/json;charset=UTF-8;Access-Control-Allow-Headers",
            'token': self.user.token,
            'User-Agent': self.userAgent
        }
        data = {
            "userId": self.lastMsg['userId'],
            "teamId": self.lastMsg['teamId'],
            "currentProvince": self.lastMsg['currentProvince'],
            "currentCity": self.lastMsg['currentCity'],
            "currentDistrict": self.lastMsg['currentDistrict'],
            "currentAddress": self.lastMsg['currentAddress'],
            "isInTeamCity": self.lastMsg['isInTeamCity'],
            "healthyStatus": self.lastMsg['healthyStatus'],
            "temperatureNormal": self.lastMsg['temperatureNormal'],
            "temperature": "37",
            "temperatureTwo": None,
            "temperatureThree": None,
            "selfHealthy": self.lastMsg['selfHealthy'],
            "selfHealthyInfo": "",
            "selfHealthyTime": None,
            "friendHealthy": 0,
            "travelPatient": self.lastMsg['travelPatient'],
            "contactPatient": self.lastMsg['contactPatient'],
            "isolation": self.lastMsg['isolation'],
            "seekMedical": self.lastMsg['seekMedical'],
            "seekMedicalInfo": "",
            "exceptionalCase": self.lastMsg['exceptionalCase'],
            "exceptionalCaseInfo": "",
            "reportDate": self.lastMsg['reportDate'],
            "currentStatus": self.lastMsg['currentStatus'],
            "villageIsCase": self.lastMsg['villageIsCase'],
            "caseAddress": None,
            "peerIsCase": self.lastMsg['peerIsCase'],
            "peerAddress": None,
            "goHuBeiCity": "",
            "goHuBeiTime": None,
            "contactProvince": "",
            "contactCity": "",
            "contactDistrict": "",
            "contactAddress": "",
            "contactTime": None,
            "diagnosisTime": None,
            "treatmentHospitalAddress": "",
            "cureTime": None,
            "abroadInfo": None,
            "isAbroad": self.lastMsg['isAbroad'],
            "isTrip": 0,
            "tripList": [],
            "peerList": [],
            "mobile": self.loginMsg['mobile']
        }
        response = requests.post(
            first_url, headers=headers, data=json.dumps(data), timeout=5)
        response_json = response.json()
        if response_json['code'] != 200:
            raise Exception("第一次上报失败，未知错误")
        else:
            return True

    @checkLogin
    def secondReport(self):
        """第二次上报方法
        ~~~
        在第一次上报的基础上进行第二次上报
        """
        if self.lastMsg == "":
            try:
                self.getLast()
            except Exception as e:
                print(e)
        second_url = f"http://hmgr.sec.lit.edu.cn/wms/addTwoHealthyRecord?healthyRecordId={self.lastMsg['id']}&temperature={self.lastMsg['temperature']}&temperatureNormal={self.lastMsg['temperatureNormal']}"
        headers = {
            'Connection': "keep-alive",
            'token': self.user.token,
            'User-Agent': self.userAgent
        }
        response = requests.put(second_url, headers=headers, timeout=5)
        response_json = response.json()
        if response_json['code'] != 200:
            raise Exception("第二次上报失败，未知错误")
        else:
            return True

    @checkLogin
    def thirdReport(self):
        """第三次上报方法
        ~~~
        在前两次上报的基础上进行第三次上报
        """
        if self.lastMsg == "":
            try:
                self.getLast()
            except Exception as e:
                print(e)
        second_url = f"http://hmgr.sec.lit.edu.cn/wms/addThreeHealthyRecord?healthyRecordId={self.lastMsg['id']}&temperature={self.lastMsg['temperature']}&temperatureNormal={self.lastMsg['temperatureNormal']}"
        headers = {
            'Connection': "keep-alive",
            'token': self.user.token,
            'User-Agent': self.userAgent
        }
        response = requests.put(second_url, headers=headers, timeout=5)
        response_json = response.json()
        if response_json['code'] != 200:
            raise Exception("第三次上报失败，未知错误")
        else:
            return True
