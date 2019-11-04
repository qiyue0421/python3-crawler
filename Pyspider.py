"""1、pyspider框架介绍"""
# pyspider是由国人binux编写的强大的网络爬虫系统，其GitHub地址为 https://github.com/binux/pyspider ，官方文档地址为：http://docs.pyspider.org/
# pyspider带有强大的WebUI、脚本编辑器、任务监控器、项目管理器以及结果处理器，它支持多种数据库后端、多种消息队列、JavaScript渲染页面的爬取，使用起来非常方便

"""pyspider基本功能
# 提供方便易用的WebUI系统，可视化地编写和调试爬虫
# 提供爬取进度监控、爬取结果查看、爬虫项目管理等功能
# 支持多种后端数据库，如MySQL、MongoDB、Redis、SQLite、Elasticsearch、PostgreSQL
# 支持多种消息队列，如RabbitMQ、Beanstalk、Redis、Kombu
# 提供优先级控制、失败重试、定时抓取等功能
# 对接了PhantomJS，可以抓取JavaScript渲染的页面
# 支持单机和分布式部署，支持Docker部署
"""


"""与Scrapy比较
# pyspider提供了WebUI，爬虫的编写、调试都是在WebUI中进行的。而Scrapy原生是不具备这个功能的，它采用的是代码和命令行操作，但可以通过对接Portia实现可视化配置
# pyspider调试非常方便，WebUI操作便捷直观。Scrapy则是使用parse命令进行调试，其方便程度不及pyspider。
# pyspider支持PhantomJS来进行JavaScript渲染页面的采集。Scrapy可以对接Scrapy-Splash组件，这需要额外配置
# pyspider中内置了pyquery作为选择器。Scrapy对接了XPath、CSS选择器和正则匹配
# pyspider的可扩展程度不足，可配置化程度不高。Scrapy可以通过对接Middleware、Pipeline、Extension等组件实现非常强大的功能，模块之间的耦合程度低，可扩展程度极高
# 综上所述：如果要快速实现一个页面的抓取，推荐使用pyspider，开发更加便捷，如快速抓取某个普通新闻网站的新闻内容。如果要应对反爬程度很强、超大规模的抓取，推荐使用Scrapy，如抓取封IP、封账号、
#           高频验证的网站的大规模数据采集
"""


"""pyspider的架构
# pyspider的架构主要分为：Scheduler(调度器)、Fetcher(抓取器)、Processer(处理器)三个部分，整个爬取过程受到Monitor(监控器)的监控，抓取的结果被Result Worker(结果处理器)处理。
# Scheduler发起任务调度，Fetcher负责抓取网页内容，Processer负责解析网页内容，然后将新生成的Request发给Scheduler进行调度，将生成的提取结果输出保存

# pyspider任务执行流程的具体过程：
# ①、每个pyspider的项目对应一个Python脚本，该脚本中定义了一个Handler类，它有一个on_start()方法。爬取首先调用on_start()方法生成最初的抓取任务，然后发送给Scheduler进行调度
# ②、Scheduler将抓取任务分发给Fetcher进行抓取，Fetcher执行并得到响应，随后将响应发送给Processer
# ③、Processer处理响应并提取出新的URL生成新的抓取任务，然后通过消息队列的方式通知Schduler当前抓取任务执行情况，并将新生成的抓取任务发送给Scheduler。如果生成了新的提取结果，则将其发送到
#     结果队列等待Result Worker处理
# ④、Scheduler接收到新的抓取任务，然后查询数据库，判断其如果是新的抓取任务或者是需要重试的任务就继续进行调度，然后将其发送回Fetcher进行抓取
# ⑤、不断重复以上工作，直到所有的任务都执行完毕，抓取结束
# ⑥、抓取结束后，程序会回调on_finished()方法，这里可以定义后处理过程
"""


"""2、pyspider的基本使用"""
"""目标"""
# 爬取去哪儿网的旅游攻略，链接为 http://travel.qunar.com/travelbook/list.htm
# 获取所有攻略的作者、标题、出发日期、人均费用、攻略正文，存储到MongoDB


"""准备工作"""
# 安装好pyspider、PhantomJS和MongoDB
# pyspider安装：pip install pyspider
# python3.7使用pyspider需要修改部分代码：https://www.jianshu.com/p/b3196d86d66f

# PhantomJS下载地址：https://phantomjs.org/download.html
# PhantomJS安装教程：https://blog.csdn.net/qq_37245397/article/details/81543450

# MongoDB下载地址：https://www.mongodb.org/downloads
# MongoDB安装教程：https://www.cnblogs.com/knowledgesea/p/4631712.html


"""启动pyspider"""
# 执行命令启动pyspider：pyspider all
# WebUI运行在 http://localhost:5000
