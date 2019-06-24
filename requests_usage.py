import requests
import re

"""GET请求"""
"""基本用法
r = requests.get('http://www.baidu.com')  # 使用get()方法请求网页，得到一个Response对象
print(type(r))
print(r.status_code)  # 状态码
print(type(r.text))  # 响应体类型是str
print(r.text)  # 响应体
print(r.cookies)  # Cookies
"""


"""
data = {
    'name': 'germey',
    'age': 22
}
r = requests.get('http://httpbin.org/get', params=data)  # 将信息数据存入字典，传给params参数构造请求链接
print(r.text)
print(type(r.text))  # str（JSON格式）
print(r.json())  # 使用json()方法将JSON格式的字符串转化为字典
print(type(r.json()))  # dict
"""


"""抓取网页
headers = {  # 构造请求头，伪装成浏览器，否则无法抓取
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)  # 构建正则表达式
titles = re.findall(pattern, r.text)  # 匹配想要的内容
print(titles)
"""


"""抓取二进制数据：图片、音频、视频
r = requests.get('https://github.com/favicon.ico')  # 抓取github站点图标
print(r.text)  # 直接输出str类型（图片直接转化为字符串）会出现乱码
print(r.content)  # 返回bytes类型数据
with open('favicon.ico', 'wb') as f:  # 以'wb'写二进制形式将bytes类型写入文件中
    f.write(r.content)
"""


"""POST请求
data = {
    'name': 'germey',
    'age': 22
}
r = requests.post('http://httpbin.org/post', data=data)  # 使用post()方法，提交数据
print(r.text)  # forms部分就是提交的数据
"""


"""响应
headers = {  # 构造请求头，伪装成浏览器，否则无法抓取
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
r = requests.get('https://www.jianshu.com')
print('Bad Request') if not r.status_code == requests.codes.ok else print('Request successfully')  # 内置状态码查询对象requests.codes，对比响应状态码是否是ok（即200）
print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)
"""


"""高级用法"""
"""文件上传
files = {'files': open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=files)  # 使用files字段传入文件
print(r.text)
"""


"""获取Cookies
headers = {  # 构造请求头，伪装成浏览器，否则无法抓取
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
r = requests.get('https://www.baidu.com', headers=headers)
print(r.cookies)  # 调用cookies属性即可成功得到Cookies
for key, value in r.cookies.items():  # 使用item()方法将cookies转化为元组组成的列表
    print(key + '=' + value)
"""


"""设置Cookie维持登录状态
headers = {  # 设置Cookie
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Host': 'www.baidu.com',
    'Cookie': 'BAIDUID=01A8B20A1F2901B0A7F7217BA3DE0455:FG=1; BIDUPSID=01A8B20A1F2901B0A7F7217BA3DE0455; PSTM=1560831709; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; '
              'yjs_js_security_passport=a50fab0591b0a989ce66e590a57bcb96119dbe24_1561301495_js; delPer=0; H_PS_PSSID=1433_21107_29135_29238_28519_29098_29131_29368_28830_29221_22157; '
              'BDUSS=BiRlRYQUg2UTRXbElya3BvWHh1TjVxblZtN2pYbXRLWkdna3NKZ0ZWcnZ6RGRkRUFBQUFBJCQAAAAAAAAAAAEAAABQBM5Ox-W358S91vHAvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
              'AAAAAAAO8~EF3vPxBdbV; BD_HOME=1; sugstore=0'
}
r = requests.get('https://www.baidu.com', headers=headers)
print(r.text)
"""


"""会话维持
s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/12345678')  # 在测试网站上设置一个名字为number的cookie，内容为12345678
r = s.get('http://httpbin.org/cookies')
print(r.text)
# 输出为：
# {
#   "cookies": {
#     "number": "12345678"
#   }
# }
"""


"""SSL证书验证
# 12306网站的证书没有被官方CA机构信任，会出现证书验证错误的结果
import urllib3

headers = {  # 构造请求头，伪装成浏览器，否则无法抓取
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
urllib3.disable_warnings()  # 设置忽略警告（没有指定证书会发出警告）
r = requests.get('https://www.12306.cn', headers=headers, verify=False)  # 将verify参数设置为False，可以避免网站证书验证错误
print(r.status_code)
"""


"""代理设置
proxies = {  # proxies参数用于设置代理，这里只是例子，需要换成有效的代理
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
    # 'http': 'http://user:password@10.10.1.10:3128/',  # 若代理需要HTTP Basic Auth，则需要使用这种语法
}
requests.get('https://www.taobao.com', proxies=proxies)
"""


"""超时设置
r = requests.get('https://www.taobao.com', timeout=1)  # 设置timeout参数，这个时间计算是发出请求到服务器返回响应的时间，超时会抛出异常
print(r.status_code)
"""


"""身份认证
from requests.auth import HTTPBasicAuth

r = requests.get('http://localhost:5000', auth=HTTPBasicAuth('username', 'password'))  # 使用requests自带的身份认证功能
# r = requests.get('http://localhost:5000', auth=('username', 'password'))  # 可以传入元组，默认使用HTTPBasicAuth类进行验证
print(r.status_code)
"""


"""Prepared Request
from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
    'name': 'germey'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
s = Session()
req = Request('POST', url, headers=headers, data=data)  # 构造Request对象，将请求当作独立的对象看待，使得进行队列调度时更加方便
prepped = s.prepare_request(req)  # 调用Session的prepare_request()方法将其转换为一个Prepared Request对象
r = s.send(prepped)  # 调用send()方法发送
print(r.text)
"""
