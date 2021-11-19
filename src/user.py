# coding: utf-8
class User:
    """用户类
    """

    def __init__(self, username: str, password: str, token: str = ""):
        """用户
        ~~~
        :param: username: 账号（学号）
        :param: password: 密码
        :param: token: 登录凭证
        """
        self.username = username
        self.password = password
        self.token = token
