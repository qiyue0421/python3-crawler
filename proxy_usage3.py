# 使用代理爬取微信公众号文章
import redis
from requests import Request
from pickle import dumps, loads


"""1、目标"""
# 利用代理爬取微信公众号的文章，提取正文、发表日期、公众号等内容，爬取来源是搜狗微信，其链接为 https://weixin.sogou.com/，然后把爬取结果保存到MySQL数据库


"""2、准备工作"""
# aiohttp、requests、redis-py、pyquery、Flask、PyMySQL


"""3、爬取分析"""
# 搜狗对微信公众平台的公众号和文章做了整合，我们可以通过上面的链接搜索到相关的公众号和文章。比如搜索 python，可以搜索到最新的文章。点击搜索后，搜索结果的URL中其实有很多无关的GET请求参数，
# 将无关参数去掉，只保留type和query参数，例如 https://weixin.sogou.com/weixin?type=2&query=python，搜索关键字为python，类型为2（2代表搜索微信文章）
# 注意，如果没有输入账号登录，那只能看到10页的内容，登录之后可以看到100页内容，如果需要爬取更多内容，就需要登录并使用Cookies来爬取。

# 搜狗微信站点的反爬虫能力很强，如连续刷新，站点就会弹出验证，网络请求出现了302跳转，返回状态码为302，跳转的链接开头为 https://weixin.sougou.com/antispider/，这是一个反爬虫验证页面。
# 所以，我们得出结论——如果服务器返回状态码为302而非200，则IP访问次数太高，IP被封禁，此请求就是失败了。如果遇到这种情况，我们可以选择识别验证码并解封，也可以使用代理直接切换IP。
# 这里采用第二种方法，使用代理直接跳过这个验证。

# 对应反爬能力很强的网站来说，如果我们遇到此种返回状态就需要重试。所以我们采用另一种爬取方式，借助数据库构造一个爬取队列，待爬取的请求都放到队列里，如果请求失败了重新放回队列，就会被重新调度爬取。
# 这里可以采用Redis的队列数据结构，新的请求就加入队列，或者有需要重试的请求也放回队列。调度的时候如果队列不为空，那就把一个个请求取出来执行，得到响应后再进行解析，提取出想要的结果。

# 这次采取MySQL存储，借助PyMySQL库，将爬取结果构造为一个字典，实现动态存储。

# 综上所述，实现的功能如下：
# ①、修改代理池检测链接为搜狗微信站点
# ②、构造Redis爬取队列，用队列实现请求的存取
# ③、实现异常处理，失败的请求重新加入队列
# ④、实现翻页和提取文章列表，并把对应请求加入队列
# ⑤、实现微信文章的信息的提取
# ⑥、将提取到的信息保存到MySQL


"""4、构造请求"""
# 既然要用队列来存储请求，那么就需要实现一个请求Request的数据结构，这个请求需要包含一些必要信息，如请求链接、请求头、请求方式、超时时间。另外，对于某个请求，我们需要实现对应的方法来处理它的响应，
# 所以，需要再加一个Callback回调函数。每次翻页请求需要代理来实现，所以还需要一个参数NeedProxy。如果一个请求失败次数太多了，那就不再重新请求了，所以还需要加失败次数的记录。
# 我们可以继承requests库中的Request对象的方式来实现这个数据结构，在它的基础上加上我们需要的额外的几个属性即可。

TIMEOUT = 10


class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback  # 回调函数
        self.need_proxy = need_proxy  # 是否需要爬取代理
        self.fail_time = fail_time  # 失败次数
        self.timeout = timeout  # 超时时间


"""5、实现请求队列"""
# 接下来需要构造请求队列，实现请求的存取。存取无非就是两个操作，一个是放，一个是取，所以这里利用Redis的rpush()和lpop()方法即可。
# 注意，存取不能直接存Request对象，Redis里面存的是字符串。所以在存Request对象之前我们先把它序列化，取出来的时候再将其反序列化，这个过程可以用pickle模块实现。
# Redis连接信息
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
REDIS_KEY = 'weixin'


class RedisQueue:
    def __init__(self):
        """
        初始化Redis
        """
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        """
        向队列添加序列化后的Request
        :param request: 请求对象
        :return: 添加结果
        """
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return: Request or None
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        """
        判断队列是否为空
        :return:
        """
        return self.db.llen(REDIS_KEY) == 0  # 判断队列长度是否为0


"""修改代理池"""
