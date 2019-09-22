# 使用Selenium爬取淘宝商品信息，并将结果保存到数据库中
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

"""1、目标
# 利用Selenium抓取淘宝商品并用pyquery解析得到商品的图片、名称、价格、购买人数、店铺名称和店铺所在地信息，并将其保存到MongoDB
"""


"""2、准备工作
# 安装Chrome浏览器并配置好ChromeDriver
# 安装Python的Selenium库
"""


"""5、获取商品列表
browser = webdriver.Chrome()  # 浏览器对象初始化，赋值为browser对象
wait = WebDriverWait(browser, 10)  # 指定最长等待时间为10秒，如果超时，直接抛出超时异常
KEYWORD = 'iPad'  # 要搜索的关键字

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):  # 保存到数据库mongoDB
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def index_page(page):  # 抓取商品索引页
    print('正在爬取第' + page + '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:  # 判断商品页码是否大于1，如果是就进行跳页操作，否则等待页面加载完成
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))  # 获取页码输入框
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))  # 获取“确认”按钮
            input.clear()  # 清空输入框
            input.send_keys(page)  # 调用send_keys方法，将页码填充到输入框中
            submit.click()  # 点击“确认”按钮
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))  # 判断高亮的页码节点是否是我们要查询的页码，证明页面跳转成功
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .item .item')))  # 每个商品的信息块是否加载完成
        get_products()  # 页面解析方法
    except TimeoutException:  # 异常处理
        index_page(page)  # 重新加载


def get_products():  # 抓取商品数据
    html = browser.page_source  # 调用page_source属性获取页码的源代码
    doc = pq(html)  # 构造PyQuery解析对象
    items = doc('#mainsrp-itemlist .items .item').items()  # 提取页面中所有商品列表
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


MAX_PAGE = 100  # 最大页数为100


def main():  # 遍历每一页
    for i in range(1, MAX_PAGE + 1):
        index_page(str(i))


main()
"""
