# coding: utf-8
from api import UserAPI
from user import User

# TODO: 填入自己的账号（学号）和密码。也许一个人用太浪费了？那就加个循环加载多个账号密码吧！
# TODO: 或者你可以关联自己的数据库，这应该是易于扩展的
if __name__ == '__main__':
    user = User(username="【账号】", password="【密码】")
    userAPI = UserAPI(user)
    userAPI.firstReport()
    userAPI.secondReport()
    userAPI.thirdReport()
