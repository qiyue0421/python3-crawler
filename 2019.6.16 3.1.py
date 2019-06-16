# 2019/6/13 开始学习爬虫
# urllib基本用法
import urllib.request
import urllib.parse
import urllib.error
import socket

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
request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
# request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36')  可以使用add_header()方法添加headers
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
"""


