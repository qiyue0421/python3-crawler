# 代理的使用
# 利用代理可以解决目标网站封IP的问题
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import socks
import socket
from urllib import request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile


"""1、代理的设置"""
"""获取代理
# 网站上有很多的代理，比如西刺代理：http://www.yunlianip.cn/，注册号即可使用
"""


"""urllib
# 假设本地安装了一部代理软件，它会在本地9743端口上创建HTTP服务，即代理为127.0.0.1:9743，另外还会在9742端口创建SOCKS代理服务，即代理127.0.0.1:9742

'''如果代理是HTTP类型
proxy = '127.0.0.1:9743'  # HTTP代理服务
# proxy = 'username:password@127.0.0.1:9743'  # 如果代理需要认证，直接加入认证用的用户名密码即可
proxy_handler = ProxyHandler({  # 设置代理，参数是字典类型，键名为协议类型，键值是代理
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)  # 调用build_opener()方法传入对象来创建一个Opener，相当于Opener已经设置好了代理
try:
    response = opener.open('http://httpbin.org/get')  # 调用open()方法，即可访问链接
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

# 运行结果是一个JSON，它有一个字段origin，标明了客户端的IP
# {
#   "args": {}, 
#   "headers": {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
#     "Accept-Encoding": "gzip, deflate", 
#     "Accept-Language": "zh-CN,zh;q=0.9", 
#     "Cache-Control": "max-age=0", 
#     "Host": "httpbin.org", 
#     "Upgrade-Insecure-Requests": "1", 
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.17 Safari/537.36"
#   }, 
#   "origin": "106.185.45.153", 
#   "url": "https://httpbin.org/get"
# }
# 
'''

'''如果代理是SOCKS5类型
# 请先下载socks.py模块，下载地址：https://sourceforge.net/projects/socksipy/files/latest/download
# 下载后将模块复制到python的安装目录下的lib文件夹中
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9742)
socket.socket = socks.socksocket
try:
    response = request.urlopen('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
'''
"""


"""requests
# 对于requests来说，代理设置更加简单，只需要传入proxies参数即可

'''如果是HTTP类型
proxy = '127.0.0.1:9743'
# proxy = 'username:password@127.0.0.1:9743'  # 如果代理需要认证，直接加入认证用的用户名密码即可
proxies = {  # 构造代理字典
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)  # 传入proxies参数
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
'''
    
'''如果是SOCKS5类型
proxy = '127.0.0.1:9743'
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy,
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
'''
"""


"""Selenium
# Selenium同样可以设置代理，包括两种方式：一种是有界面浏览器，以Chrome为例；另一种是无界面浏览器，以PhantomJS为例

'''Chrome
proxy = '127.0.0.1:9743'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')
'''

'''Chrome认证代理（复杂）
ip = '127.0.0.1'
port = 9743
username = 'foo'
password = 'bar'

manifest_json = '''
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    }
}
'''

background_js = '''
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%(ip)s",
            port: %(port)s
            }
        }
    }

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%(username)s",
            password: "%(password)s"
        }
    }
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
)
''' % {'ip': ip, 'port': port, 'username': username, 'password': password}

plugin_file = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_extension(plugin_file)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')
'''

'''PhantomJS
service_args = [
    '--proxy=127.0.0.1:9743',
    '--proxy-type=http'
    '--proxy-auth=username:password'  # 设置认证
]
browser = webdriver.PhantomJS(service_args=service_args)
browser.get('http://httpbin.org/get')
print(browser.page_source)
'''
"""
