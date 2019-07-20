from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient
"""Ajax定义"""
# Ajax，即异步的JavaScript和XML，利用JavaScript在保证页面不被刷新、页面链接不改变的情况下与服务器交换数据并更新部分网页的技术


"""Ajax基本原理"""
# 发送请求
# 解析内容
# 渲染页面


"""Ajax实例
# 模拟Ajax请求爬取微博
base_url = 'https://m.weibo.cn/api/container/getIndex?'
uuid = '5138617574'  # 微博用户的个人唯一表示
# uuid = '2830678474'

headers = {
    'Host': 'm.weibo.cn',
    # 'Referer': 'https://m.weibo.cn/u/2830678474',
    'Referer': 'https://m.weibo.cn/u/' + uuid,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def total_pages():  # 获取微博总条数
    json = get_page()
    item = json.get('data').get('cardlistInfo').get('total')
    pages = int(item / 10) + 1
    return pages


def get_page(page=1):  # 获取每次Ajax请求的结果，唯一参数为页数page，一页为10条微博
    params = {  # 构造请求字典
        'type': 'uid',
        'value': uuid,
        'containerid': '107603' + uuid,
        'page': page
    }
    url = base_url + urlencode(params)  # 使用urlencode()方法将字典类型序列化为GET请求参数，构造链接
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=2830678474&containerid=1005052830678474
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # 将响应内容解析为JSON格式
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):  # 解析结果，提取信息
    if json:
        items = json.get('data').get('cards')  # 通过get()方法获取对应键名的内容，即10条微博内容
        for item in items:
            item = item.get('mblog')  # 获取mblog分组，即主题部分
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()  # 微博正文，使用pyquery去掉正文的HTML标签，直接获取纯文本内容
            weibo['attitudes'] = item.get('attitudes_count')  # 点赞数
            weibo['comments'] = item.get('comments_count')  # 评论
            weibo['reposts'] = item.get('reposts_count')  # 转发数
            yield weibo


client = MongoClient()
db = client['weibo']
collection = db['weibo']


def save_to_mongo(result):  # 保存到mongo数据库中
    if collection.insert_one(result):
        print('Saved to Mongo')


if __name__ == '__main__':
    pages = total_pages()
    for page in range(1, pages + 1):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
            save_to_mongo(result)
"""
