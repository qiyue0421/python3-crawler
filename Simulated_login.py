# 模拟登录
import requests
from lxml import etree

"""1、模拟登录并爬取GitHub"""
"""本节目标"""
# 以GitHub为例来实现模拟登录的过程，同时爬取登录后才可以访问的页面信息，如好友动态、个人信息等内容

"""环境准备"""
# 安装requests库和lxml库

"""代码实战"""
class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()  # 维持一个会话并且自动处理Cookies

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')[0]  # 获取authenticity_token信息
        return token

    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)

    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)

    def login(self, email, password):
        post_data = {  # 构造表单
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)  # post()方法模拟登录，requests自动处理了重定向信息，登录成功后自动跳转到首页
        if response.status_code == 200:
            self.dynamics(response.text)

        response = self.session.get(self.logined_url, headers=self.headers)  # 请求个人详情页
        if response.status_code == 200:
            self.profile(response.text)  # 处理个人详情页信息


if __name__ == '__main__':
    login = Login()
    login.login(email='qiyue0421', password='lspLSP0421')
