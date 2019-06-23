# 2019/6/13 开始学习爬虫
# urllib库基本用法

import urllib.request
import urllib.parse   # parse模块定义了处理URL的标准接口
import urllib.error
import socket
from urllib.error import URLError
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, ProxyHandler
import http.cookiejar


"""1、发送请求"""
"""urlopen()方法
response = urllib.request.urlopen('https://www.python.org')  # 抓取python官网
print(response.read().decode('utf-8'))
print(type(response))  # <class 'http.client.HTTPResponse'>
print(response.status)  # 响应状态码
print(response.getheaders())  # 响应头
print(response.getheader('Server'))  # 获取响应头参数Server的值
"""


"""data参数
data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')  # urlencode方法将字典参数转换为str字符串类型，bytes使用utf-8编码格式将字符串转换为bytes类型
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())
"""


"""timeout参数
response = urllib.request.urlopen('http://httpbin.org/get', timeout=1)  # timeout参数用来设置超时时间，如果没有得到响应，则会抛出URLError异常
print(response.read())
"""


"""捕获timeout异常
try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)  # 设置超时时间为0.1秒
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):  # 判断异常是否是socket.timeout类型（超时异常）
        print('Time out!')
"""


"""Request类
request = urllib.request.Request('https://python.org')  # 使用Request类构建一个完整的请求
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
"""


"""使用多个参数构建Request类
url = 'http://httpbin.org/post'
headers = {  # 请求头
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',  # 伪装浏览器
    'Host': 'httpbin.org'
}

cat_dict = {'name': 'qiyue'}  # 提交的信息
data = bytes(urllib.parse.urlencode(cat_dict), encoding='utf8')  # 转换为bytes类型

request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')  # 构建请求
# request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36')  可以使用add_header()方法添加headers
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
"""


"""高级用法-handler
username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)  # 添加用户名和密码，建立一个处理验证的handler
auth_handler = HTTPBasicAuthHandler(p)  # 实例化对象,用于管理认证，参数为HTTPPasswordMgrWithDefaultRealm对象
opener = build_opener(auth_handler)  # 构建Opener,在发送请求时相当于已经验证成功了

try:
    result = opener.open(url)  # 打开链接
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)
"""


"""代理
proxy_handler = ProxyHandler({
    'http': 'http://127.0.0.1:9743',  # 本地搭建一个代理，运行在9743端口上
    'https': 'https://127.0.0.1:9743'  # 参数为一个字典，键名是协议类型（http https），键值为代理链接
})
opener = build_opener(proxy_handler)  # 构造opener
try:  # 异常处理模块
    response = opener.open('https://www.baidu.com')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
"""


"""Cookies
cookie = http.cookiejar.CookieJar()  # 首先声明一个CookieJar对象
handler = urllib.request.HTTPCookieProcessor(cookie)  # 构建handler
opener = build_opener(handler)  # 利用handler构建opener
response = opener.open('http://wwww.baidu.com')
for item in cookie:
    print(item.name + "=" + item.value)
"""


"""Cookies输出不同格式
filename = 'cookies.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)  # txt文档格式
cookie = http.cookiejar.LWPCookieJar(filename)  # LWP格式
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = build_opener(handler)
respnse = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)  # 使用save()方法保存为本地Cookies文件
"""


"""读取Cookies文件
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)  # 使用load()方法读取本地的Cookies文件
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = build_opener(handler)
response = opener.open('http://wwww.baidu.com')
print(response.read().decode('utf-8'))
"""


"""2、处理异常"""
"""URLError
try:
    response = urllib.request.urlopen('http://www.imooc.com/qiyue.html')
except URLError as e:  # URLError类继承自OSError这个异常模块的基类，由request模块产生的异常都可以通过捕获这个异常来处理
    print(e.reason)  # reason属性
"""


"""HTTPError
try:
    urllib.request.urlopen('http://www.imooc.com/qiyue.html')
except urllib.error.HTTPError as e:  # HTTPError是URLError的子类，专门用来处理HTTP请求错误，比如认证失败
    print(e.reason, e.code, e.headers, sep='\n')   # 查看类中的三个属性，分别输出错误原因、HTTP返回状态码、请求头
except urllib.error.URLError as e:  # 捕获完子类的异常后，再去捕获父类的错误
    print(e.reason)
else:  # 处理正常的逻辑
    print('Request Successfully')
"""


"""3、解析链接"""
"""urlparse()
result = urllib.parse.urlparse('http://www.baidu.com/index.html;user?id=5#comment')  # parse模块定义了处理URL的标准接口，urlparse()方法实现URL的识别和分段
print(type(result), result)
# 输出为：
# <class 'urllib.parse.ParseResult'>  # 返回一个ParseResult对象，实际上是一个元组，可以用索引顺序获取，也可以用属性名获取
# ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment')
#
# scheme:协议
# netloc:域名
# path:访问路径
# params:参数
# query:查询条件
# fragment:锚点，用于直接定位页面内部的下拉位置
#
# 一个标准的链接格式：scheme://netloc/path;params?query#fragment
"""


"""urlunparse()
data = ['https', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']  # 接受的参数为一个可迭代对象，且必须长度必须是6，否则将会异常
print(urllib.parse.urlunparse(data))  # urlunparse()方法实现URL的构造
# 输出为：
# https://www.baidu.com/index.html;user?a=6#comment
"""


"""urlsplit()
from urllib.parse import urlsplit
result = urlsplit('http://www.baidu.com/index.html;user?a=6#comment')  # 与urlparse()类似，但是不单独解析params这一部分（合并到path中），只返回5个结果
print(result)
# 输出为：
# SplitResult(scheme='http', netloc='www.baidu.com', path='/index.html;user', query='a=6', fragment='comment')  # 返回的是一个元组，可以使用属性和索引来获取值 
"""


"""urlunsplit()
from urllib.parse import urlunsplit
data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']  # 接受的参数为一个可迭代对象，且必须长度必须是5，否则将会异常
print(urlunsplit(data))  # 与urlunparse()类似，唯一区别是接受的参数个数必须为5
# 输出为：
# http://www.baidu.com/index.html?a=6#comment
"""


"""urljoin()
from urllib.parse import urljoin  # 用于生成链接
print(urljoin('http://www.baidu.com', 'FAQ.html'))  # 第一个参数为base_url，第二个参数为新的链接，该方法会分析base_url中的协议、域名、路径三个部分，并对新链接缺失的部分进行补充
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))  # 如果三个部分不在新链接，则使用base_url补充新链接；如果新链接中三个部分都存在，则直接使用新链接
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#comment', '?category=2'))
# 输出为：
# http://www.baidu.com/FAQ.html
# https://cuiqingcai.com/FAQ.html
# https://cuiqingcai.com/FAQ.html
# https://cuiqingcai.com/FAQ.html?question=2
# https://cuiqingcai.com/index.php
# www.baidu.com?category=2#comment
# www.baidu.com?category=2
"""


"""urlencode()  # 序列化
from urllib.parse import urlencode

params = {
    'name': 'germey',
    'age': 22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)  # 将字典类型序列化为GET请求参数
print(url)
# 输出为：
# http://www.baidu.com?name=germey&age=22
"""


"""parse_qs()、parse_qsl()  # 反序列化
from urllib.parse import parse_qs, parse_qsl

query = 'name=germey&age=22'
print(parse_qs(query))  # 将GET请求参数转化为字典
print(parse_qsl(query))  # 将GET请求参数转化为元组
# 输出为：
# {'name': ['germey'], 'age': ['22']}
# [('name', 'germey'), ('age', '22')]
"""


"""quote()、unquote()  # url编码
from urllib.parse import quote, unquote

keyword = '壁纸'
url = 'https://www.baidu.com/s?wd=' + quote(keyword)  # 将中文字符转为URL编码
print(url)
print(unquote(url))  # 还原中文字符
# 输出为：
# https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8
# https://www.baidu.com/s?wd=壁纸
"""


"""4、分析Robots协议"""
"""robotparser
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url('https://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'https://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'https://www.jianshu.com/search?q=python&page=1&type=collections'))
"""
