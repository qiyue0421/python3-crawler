# 使用代理爬取微信公众号文章
import redis
import requests
from requests import Request, Session,ReadTimeout, ConnectionError
from urllib.parse import urlencode
from pickle import dumps, loads
from pyquery import PyQuery as pq
import pymysql

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
PROXY_POOL_URL = 'http://127.0.0.1:5555/random'


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


"""6、实现MySQL存储模块"""
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'weixin'
# 手动创建数据库weixin
"""
create database weixin; 
"""

# 新建一个数据表名为article
"""
create table `article` (
    `id` int(11) not null,
    `title` varchar(255) not null,
    `content` text not null,
    `data` varchar(255) not null ,
    `wechat` varchar(255) not null ,
    `nickname` varchar(255) not null
) default charset=utf8;
alter table `article` add primary key (`id`);
"""


class MySQL:
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT, database=MYSQL_DATABASE):
        """
        MySQL初始化
        :param host:
        :param username:
        :param password:
        :param port:
        :param database:
        """
        try:
            self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def insert(self, table, data):
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        keys = ','.join(data.keys())
        value = ','.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, value)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()


"""7、第一个请求"""
# 构造第一个请求放到队列里以供调度


class Spider:
    # 设置全局变量
    base_url = 'https://weixin.sogou.com/weixin'
    keyword = 'python'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'ABTEST=4|1571841717|v1; IPLOC=CN4404; SUID=9FEC49DF4842910A000000005DB066B5; SUID=9FEC49DF3120910A000000005DB066B5; weixinIndexVisited=1; SUV=006315DEDF49EC9F5DB066B6BA46D980; '
                  'sct=1; PHPSESSID=90i0r29ndggeup072jtbdfir53; SNUID=E49732A47B7EEED254975B6A7B8AFE3C; successCount=1|Thu, 24 Oct 2019 13:46:17 GMT; JSESSIONID=aaa4hMDT2oPOwdMdfr93w; '
                  'ppinf=5|1571924583|1573134183'
                  '|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0OkZpbmV8Y3J0OjEwOjE1NzE5MjQ1ODN8cmVmbmljazo0OkZpbmV8dXNlcmlkOjQ0Om85dDJsdU0yZ2p3R3ZvSV8yTW5CY1lxWTNsQUlAd2VpeGluLnNvaHUuY29tfA; '
                  'pprdig=sAUW5bZURcAs5cCQNo5DSGpMN401FEY49f9eibusHbhBvd34_lVZnMJjvKN_BrH6uDeYOMgMWty_QQHx8ajZQzEb-AfXJGWC8FIjiS0QkmQST8SGd75vm-kx1U887fKnDLZxHXD4HV1ZVNgtqYQtfA5qKe8xQ-J9J58UXlmFZoQ'
                  '; sgid=06-41818573-AV2xqme8NOB1iafVfZEQ1vd4; ppmdig=157192458300000075cc6c1e341c63703a29581762789e66 ',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    session = Session()  # 执行请求
    queue = RedisQueue()  # 存储请求
    mysql = MySQL()
    VALID_STATUSES = [200]  # 成功状态码
    MAX_FAILED_TIME = 20  # 最大请求失败次数

    def start(self):
        """
        初始化工作
        :return:
        """
        # 全局更新Headers
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})  # 构造起始URL

        # 构造WeixinRequest对象，回调函数是Spider类的parse_index()方法，也就是当这个请求成功以后就用parse_index()来处理解析
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)

        # 调度第一个请求
        self.queue.add(weixin_request)

    def get_proxy(self):  # 获取随机可用代理
        """
        从代理池获取代理
        :return:
        """
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get Proxy', response.text)
                return response.text
            return None
        except requests.ConnectionError:
            return None

    def schedule(self):
        """
        调度请求
        :return:
        """

        while not self.queue.empty():  # 队列不为空
            weixin_request = self.queue.pop()  # 取出下一个请求
            callback = weixin_request.callback
            print('Schedule', weixin_request.url)
            response = self.request(weixin_request)  # 执行请求
            if response and response.status_code in self.VALID_STATUSES:
                results = list(callback(response))  # 获取本页所有微信文章链接
                if results:
                    for result in results:
                        print('New Result', result)
                        if isinstance(result, WeixinRequest):  # 结果是WeixinRequest，就将其重新加入队列
                            self.queue.add(result)
                        if isinstance(result, dict):  # 如果是文章详情页的内容，则存储到mysql中
                            self.mysql.insert('articles', result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def parse_index(self, response):
        """
        解析索引页
        :return: 新的响应
        """
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield weixin_request

    def parse_detail(self, respnse):
        """
        解析详情页
        :param respnse: 响应
        :return: 微信公众号文章内容
        """
        doc = pq(respnse.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#publish_time').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(1) > span').text()
        }
        yield data

    def request(self, weixin_request):
        """
        执行请求
        :param weixin_request: 请求
        :return: 响应
        """
        try:
            if weixin_request.need_proxy:  # 判断是否需要代理
                proxy = self.get_proxy()  # 调用get_proxy()方法获取代理
                # proxy = '211.101.154.105:43598'
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    print(self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies))
                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def error(self, weixin_request):
        """
        错误处理
        :param weixin_request: 请求
        :return:
        """
        weixin_request.fail_time = weixin_request.fail_time + 1
        print('Request Failed', weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < self.MAX_FAILED_TIME:
            self.queue.add(weixin_request)

    def run(self):
        """
        入口
        :return:
        """
        self.start()
        self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.run()

# 总的来说，大部分模块基本实现，但是现阶段搜狗的反爬虫太厉害导致程序未能运行成功，实力有限暂且学习吧！
