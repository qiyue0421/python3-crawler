# 代理池的维护
import json
import time
import redis
import requests
import aiohttp
import asyncio
from requests.exceptions import ConnectionError
from random import choice
from pyquery import PyQuery as pq
from flask import Flask, g
from multiprocessing import Process

try:
    from aiohttp import ClientError
except Exception as e:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

"""2、搭建一个高效易用的代理池"""
"""代理池的目标
# 基本模块分为4块：存储模块、获取模块、检测模块、接口模块
# 存储模块：负责存储抓取下来的代理。首先要保证代理不重复，要标识代理的可用情况，还要动态实时处理每个代理，所以一种比较高效的存储方式是使用Redis的Sorted Set，即有序集合

# 获取模块：需要定时在各大代理网站抓取代理。代理可以是免费公开代理也可以是付费代理，代理的形式都是IP加端口，此模块尽量从不同来源获取，尽量抓取高匿代理，抓取成功之后将可用代理保存到数据库中。

# 检测模块：需要定时检测数据库中的代理。这里需要设置一个检测链接，最好是爬取哪个网站就检测哪个网站，这样更加有针对性，如果要做一个通用型的代理，那可以设置百度等链接来检测。
#           另外，需要标识每一个代理的状态，如设置分数标识，100分代表可用，分数越少代表越不可用。检测一次，如果代理可用，则将分数标识立即设置为100满分，也可以在原基础上加1分；
#           如果代理不可用，可以将分数标识减1分，当分数减到一定阈值后，代理就直接从数据库移除。通过这样的标识分数，可以辨别代理的可用情况，选用的时候更有针对性。

# 接口模块：需要用API来提供对外服务的接口。其实可以直接连接数据库来取对应的数据，但是这样就需要知道数据库的连接信息，并且要配置连接，而比较安全和方便的方式就是提供一个Web API接口，
#           通过访问接口即可拿到可用代理。另外，由于可用代理可能有多个，那么可以设置一个随机返回某个可用代理的接口，这样就能保证每个可用代理都可以被取到，实现负载均衡。
"""


"""代理池的架构
# 代理池分为4个模块：存储模块、获取模块、检测模块、接口模块
# 存储模块使用Redis的有序集合，用来做代理的去重和状态标识，同时它也是中心模块和基础模块，将其他模块串联起来
# 获取模块定时从代理网站获取代理，将获取的代理传递给存储模块，并保存到数据库
# 检测模块定时通过存储模块获取所有代理，并对代理进行检测，根据不同的检测结果对代理设置成不同的标识
# 接口模块通过Web API提供服务接口，接口通过连接数据库并通过Web形式返回可用的代理
"""


"""代理池的实现"""
"""存储模块"""
# 使用Redis的有序集合，集合的每一个元素都是不重复的，对于代理池来说，集合的元素就变成了一个个代理，也就是IP+PORT的形式，如60.207.237.111：8888，这样的一个代理就是集合的一个元素。
# 另外，有序集合的每一个元素都有一个分数字段，分数是可以重复的，可以使浮点数类型，也可以是整数类型。该集合会根据每一个元素的分数对集合进行排序，数值小的排在前面，数值大的排在后面，
# 这样就实现了集合元素的排序。

# 对于代理池来说，这个分数可以作为判断一个代理是否可用的标志，100为最高分，代表最可用，0为最低分，代表最不可用。如果要获取可用代理，可以从代理池中随机获取分数最高的代理，注意是随机，
# 这样可以确保每个可用代理都会被调用到。

# 设置分数的规则：
# 1、分数100为可用，检测器会定时循环检测每个代理可用情况，一旦检测到有可用的代理就立即置为100，检测到不可用就将分数减1，分数减少到0后将代理移除
# 2、新获取的代理的分数为10，如果测试还行，分数立即置为100，不可行则分数减1，分数减少到0后将代理移除

MAX_SCORE = 100  # 最大分数
MIN_SCORE = 0  # 最小分数
INITIAL_SCORE = 10  # 初始分数
# Redis连接信息
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
# 有序集合的键名，通过它来获取代理存储所使用的有序集合
REDIS_KEY = 'proxies'


class RedisClient(object):  # RedisClient类用于操作Redis的有序集合
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)  # 初始化一个StrictRedis类，传入连接信息常量，建立Redis连接

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数（默认为初始分数）
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则抛出异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)  # 获取100分的代理
        if len(result):
            return choice(result)  # 获取成功则随机返回一个
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)  # 按照排名获取前100名
            if len(result):
                return choice(result)  # 再次随机返回一个
            else:
                # raise PoolEmptyError
                print('Error!')

    def decrease(self, proxy):
        """
        代理无效则代理值减一分，如果分数值小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在集合中
        :param proxy:代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理有效时将代理设置为MAX_SCORE，即100
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取当前集合的元素个数
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理列表，以供检测使用
        :return: 全部代理
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


"""检测模块"""
base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.17 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options=None):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    if options is None:
        options = {}
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None


class ProxyMetaclass(type):  # 定义一个元类，获取所有以crawl开头的方法名称
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():  # 遍历attrs参数可以获取类的所有方法信息
            if 'crawl_' in k:  # 判断方法的开头是否为crawl
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(mcs, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):  # 抓取代理类
    def get_proxies(self, callback):  # 将类中所有以crawl开头的方法都调用一遍，获取每个方法返回的代理并组合成列表形式返回
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count：页码
        :return：代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        """
        获取代理66
        :return：代理
        """
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')


# 设定代理池阈值
POOL_UPPER_THRESHOLD = 1000


class Getter:  # 获取器类
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):  # 动态地调用所有以crawl开头的方法，然后获取抓取到的代理，将其加入到数据库存储起来
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlerFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)


"""检测模块"""
# 由于代理的数量非常多，为了提高代理的检测效率，使用异步请求库aiohttp来进行检测
VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):  # 定义一个异步方法用来检测单个代理的可用情况
        """
        测试单个代理
        :param proxy: 单个代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)  # 可用则代理分数为100
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)  # 不可用代理分数减1
                        print('请求响应吗不合法', proxy)
            except (ClientError, aiohttp.client.ClientConnectionError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败')

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):  # 一次测试100个
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))  # 分配任务，启动运行
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)


"""接口模块"""
__all__ = ['app']
app = Flask(__name__)  # 声明一个Flask对象


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')  # 首页接口
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')  # 随机代理页接口
def get_proxy():
    """
    获取随机可用代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')  # 获取数量页
def get_counts():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


'''
if __name__ == '__main__':
    app.run()
'''


"""调度模块"""
TESTER_CYCLE = 20  # 测试模块休眠时间
GETTER_CYCLE = 20  # 获取模块休眠时间
TESTER_ENABLED = True  # 测试模块开关
GETTER_ENABLED = True  # 获取模块开关
API_ENABLED = True  # 接口模块开关
# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555


class Scheduler:
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 休眠时间
        :return: None
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 休眠时间
        :return: None
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        :return: None
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()


scheduler = Scheduler()
scheduler.run()
