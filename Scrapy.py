"""1、Scrapy框架介绍"""
# Scrapy是一个基于Twisted的异步处理框架，是纯Python实现的爬虫框架，其架构清晰，模块之间耦合程度低，可扩展性极强，可以灵活完成各种需求。我们只需要定制
# 开发几个模块就可以轻松实现一个爬虫，几乎可以应对所有反爬网站，是目前Python中使用最广泛的爬虫框架

"""架构介绍
# Scrapy主要分为如下几个部分：
# Engine：引擎，处理整个系统的数据流处理、触发事务，是整个框架的核心
# Item：项目，它定义了爬取结果的数据结构，爬取的数据会被赋值成该Item对象
# Scheduler：调度器，接受引擎发过来的请求并将其加入到队列中，在引擎再次请求的时候将请求提供给引擎
# Downloader：下载器，下载网页内容，并将网页内容返回给蜘蛛
# Spiders：蜘蛛，其内定义了爬取的逻辑和网页的解析规则，主要负责解析响应并生成提取结果和新的请求
# Item Pipeline：项目管道，负责处理由蜘蛛从网页中抽取的项目，主要任务是清洗、验证和存储数据
# Downloader Middlewares：下载器中间件，位于引擎和下载器之间的钩子框架，主要处理引擎与下载器之间的请求及响应
# Spider Middlewares：蜘蛛中间件，位于引擎和蜘蛛之间的钩子架构，主要处理向蜘蛛输入的响应和输出的结果及新的请求
"""


"""数据流
# Scrapy中的数据流由引擎控制，数据流的过程如下：
# ①、Engine首先打开一个网站，找到处理该网站的Spider，并向该Spider请求第一个要爬取的URL
# ②、Engine从Spider中获取到第一个要爬取的URL，并通过Scheduler以Request的形式调度
# ③、Engine向Scheduler请求下一个要爬取的URL
# ④、Scheduler返回下一个要爬取的URL给Engine，Engine将URL通过Downloader Middlewares转发给Downloader下载
# ⑤、一旦页面下载完毕，Downloader生成该页面的Response，并将其通过Downloader Middlewares发送给Engine
# ⑥、Engine从下载器中接收到Response，并将其通过Spider Middlewares发送给Spider处理
# ⑦、Spider处理Response，并返回提取到的Item及新的Request给Engine
# ⑧、Engine将Spider返回的Item给Item Pipeline，将新的Request给Scheduler
# ⑨、重复步骤②~⑧，直到Scheduler中没有更多的Request，Engine关闭该网站，爬取结束
# 通过多个组件的相互协作、不同组件完成工作的不同、组件对异步处理的支持，Scrapy最大限度地利用了网络带宽，大大提高了数据爬取和处理的效率
"""


"""项目结构
# Scrapy框架和pyspider不同，它是通过命令行来创建项目的，代码的编写还是需要IDE。项目创建后，项目文件结构如下所示：
# scrapy.cfg
# project/
#     __init__.py
#     items.py
#     pipelines.py
#     settings.py
#     middlewares.py
#     spiders/
#         __init__.py
#         spider1.py
#         spider2.py
#         ...
#
# 各个文件功能描述如下：
# scrapy.cfg：它是Scrapy项目的配置文件，其内定义了项目的配置文件路径、部署相关信息等内容
# items.py：它定义了Item数据结构，所有的Item的定义都可以放在这里
# pipelines.py：它定义了Item Pipeline的实现，所有的Item Pipeline的实现都可以放在这里
# settings.py：它定义了项目的全局配置
# middlewares.py：它定义了Spider Middlewares和Downloader Middlewares的实现
# spiders：其内包含一个个Spider的实现，每个Spider都有一个文件
"""


"""2、Scrapy入门"""
"""本节目标
# 本节要完成的目标如下：
# ①、创建一个Scrapy项目
# ②、创建一个Spider来抓取站点和处理数据
# ③、通过命令行将抓取的内容导出
# ④、将抓取的内容保存到MongoDB数据库
"""


"""准备工作
# 安装好Scrapy框架、MongoDB和PyMongo库
# Scrapy框架安装步骤：
#     安装lxml：pip install lxml
#     安装pyOpenSSL：pip install pyOpenSSL
#     安装Twisted：pip install Twisted
#     安装Scrapy：pip install Scrapy
"""


"""创建项目
# 创建一个Scrapy项目，项目文件可以直接用scrapy命令生成，命令如下：
# scrapy startproject tutorial
# 这个命令会创建一个名为 tutorial 的文件夹
"""


"""创建Spider
# Spider是自己定义的类，Scrapy用它来从网页里抓取内容，并解析抓取的结果。不过这个类必须继承Scrapy提供的Spider类scrapy.Spider，还要定义Spider的名称和起始请求以及怎样处理爬取后的结果的方法
#
# 也可以使用命令行创建一个Spider，比如要生成Quotes这个Spider，可以执行如下命令：
# cd tutorial
# scrapy genspider quotes quotes.toscrape.com
# 进入刚才创建的tutorial文件夹，然后执行genspider命令，第一个参数是Spider的名称，第二个参数是网站域名。执行完毕后，spiders文件夹中多了一个quotes.py，
# 其内容如下：

class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # 每个项目的唯一名字，用来区分不同的Spider
    allowed_domains = ['quotes.toscrape.com']  # 允许爬取的域名，如果初始或后续的请求链接不是这个域名下的，则请求链接会被过滤掉
    start_urls = ['http://quotes.toscrape.com/']  # 包含了Spider在启动时爬取的url列表，初始请求是由它来定义的
    
    # 该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求
    def parse(self, response):  # 默认情况下，被调用时start_urls里面的链接构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数
        pass

"""


"""创建Item
# Item是保存爬取数据的容器，它的使用方法和字典类似，不过，相比字典，Item多了额外的保护机制，可以避免拼写错误或者定义字段错误
# 创建Item类需要继承scrapy.Item类，并且定义类型为scrapy.Field的字段。
# 假设目标网站可以获取的内容有text、author、tags，将items.py修改如下：

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

"""


"""解析Response
# quotes.py文件中的parse()方法的参数response是start_urls里面的链接爬取后的结果。所以在parse()方法中，我们可以直接对response变量包含的内容进行解析，比如浏览请求结果的网页源代码，
# 或者进一步分析源代码的内容，或者找出结果中的链接而得到下一个请求
#
# 分析网站 http://quotes.toscrape.com/ 的源代码可以看出，每一页都有多个class为quote的区块，每个区块内都包含text、author、tags，那么我们先找出所有的quote，然后提取每个quote中的内容
# 提取的方式可以是CSS选择器或XPath选择器，在这里我们使用CSS选择器，parse()方法改写如下：

def parse(self, response):
    quotes = response.css('.quote')  # 首先选取所有的quote，并将其赋值为quotes变量
    for quote in quotes:
        text = quote.css('.text::text').extract_first()  # 获取结果列表的第一个元素
        author = quote.css('.author::text').extract_first()
        tags = quote.css('.tags .tag::text').extract()  # 获取所有结果组成的列表

"""


"""使用Item
# 定义了Item，接下来就要使用它，Item可以理解为一个字典，不过在声明的时候需要实例化。然后依次用刚才解析的结果赋值Item的每一个字段，最后将Item返回即可

from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')  # 首先选取所有的quote，并将其赋值为quotes变量
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()  # 获取结果列表的第一个元素
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()  # 获取所有结果组成的列表
            yield item
            
"""


"""后续的Request
# 以上操作实现了从初始页面抓取内容，那么下一页的内容该如何抓取？这需要从当前页面中找到信息来生成下一个请求，然后在下一个请求的页面里找到信息再构造再下一个请求，这样循环往复迭代，从而实现整站爬取
# 将源代码页面拉取到最底下，发现有一个名为Next的按钮，查看它的链接是 /page/2/，全链接就是 http://quotes.toscrape.com/page/2，通过这个链接我们就可以构造下一个请求了
#
# 构造请求时需要用到scrapy.Request，这里我们传递两个参数——url和callback，这两个参数的说明如下：
# ①、url：请求链接
# ②、callback：回调函数，指定了该回调函数的请求完成之后，获取到响应，引擎会将该响应作为参数传递给这个回调函数。回调函数进行解析或生成下一个请求，回调函数如上文的parse()所示
#
# 代码实现如下：

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')  # 首先选取所有的quote，并将其赋值为quotes变量
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()  # 获取结果列表的第一个元素
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()  # 获取所有结果组成的列表
            yield item
        next = response.css('.pager .next a::attr("href")').extract_first()  # 首先使用CSS选择器获取下一个页面的链接，然后再调用extract_first()方法获取内容
        url = response.urljoin(next)  # 使用urljoin()方法将相对URL构造成一个绝对URL
        # 通过url和callback变量构造了一个新的请求，这个请求完成后，响应会重新经过parse方法处理，得到第二页的解析结果，然后生成第二页的下一页，也就是第三页的请求，这样就进入了一个循环，直到最后一页
        yield scrapy.Request(url=url, callback=self.parse)  

"""


"""运行"""
# 进入目录，运行如下命令：
# scrapy crawl quotes
# 就可以看到结果了
#
