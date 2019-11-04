# Cookies池的搭建
import redis
import random


"""1、本节目标"""
# 以新浪微博为例实现一个Cookies池的搭建过程，具有以下几个特点：
# ①、Cookies池中保存了许多新浪微博账号和登录后的Cookies的信息
# ②、Cookies池需要定时检测每个Cookies的有效性，如果某个Cookies无效，那就删除该Cookies并模拟登录生成新的Cookies
# ③、Cookies池还需要一个非常重要的接口，即获取随机Cookies的接口，Cookies运行之后，我们只需要请求该接口，即可随机获得一个Cookies并用其爬取
# 综上所述，Cookies池需要有自动生成Cookies、定时检测Cookies、提供随机Cookies等几大核心功能


"""2、准备工作"""
# 一些微博账号、Redis数据库、redis-py、requests、Selelnium和Flask库、Chrome浏览器配置好ChromeDriver


"""3、Cookies池架构"""
# Cookies池的基本模块分为4个核心模块：存储模块、生成模块、检测模块和接口模块
# 存储模块：负责存储每个账号的用户名和密码以及每个账号对应的Cookies信息，同时还需要提供一些方法来实现方便的存取操作
# 生成模块：负责生成新的Cookies，此模块会从存储模块逐个拿取账号的用户名和密码，然后模拟登录目标页面，判断登录成功，就将Cookies返回并交给存储模块存储
# 检测模块：定时检测数据库中的Cookies，在这里需要设置一个检测模块，不同的站点检测链接不同，检测模块会逐个拿取账号对应的Cookies去请求链接，如果返回的状态是有效的，那么此Cookies没有失效，否则
#           Cookies失效并移除，接下来等待生成模块重新生成即可
# 接口模块：需要用API来提供对外服务的接口。由于可用的Cookies可能有多个，我们随机返回Cookies的接口，这样可以保证每个Cookies都有可能被取到。Cookies越多，每个Cookies被选到的概率就越小，从而减少封号危险


"""代码实现"""
"""4、存储模块"""
# 存储账号信息和Cookies信息
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param type:
        :param website:
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        # 如果是存储账户的Hash，那么type和website表示为：accounts:weibo；如果是存储Cookies的Hash，那么此处的type和website表示为：cookies:weibo
        self.type = type  # 类型
        self.website = website  # 站点名称

    def name(self):
        """
        获取Hash的名称(即key的名称）
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或Cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self,username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取键的数目
        :return: 数目
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.name())


"""5、生成模块"""
# 负责获取各个账号信息并模拟登录，随后生成Cookies并保存
