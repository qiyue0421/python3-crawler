# 实例1：抓取猫眼电影排行TOP100的相关内容
# 工具：requests库及正则表达式
# 抓取分析
# 1、抓取目标站点为：https://maoyan.com/board/4，打开后显示榜单消息
# 2、网站有分页，每页显示10个，https://maoyan.com/board/4?offset=10显示的是第二页的内容
# 3、offset代表偏移量值，如果偏移量为n，则显示的电影序号就是n+1到n+10，获取TOP100只需要分开请求10次

import requests
import re
import json
import time


def get_one_page(url):  # 获取响应页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    response = requests.get(url, headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):  # 使用正则表达式解析页面，提取有用内容
    regex1 = r'<dd>.*?board-index.*?>(.*?)</i>'  # 提取排名信息
    regex2 = r'.*?data-src="(.*?)"'  # 提取图片
    regex3 = r'.*?name.*?<a.*?>(.*?)</a>'  # 提取电影名字
    regex4 = r'.*?star">(.*?)</p>'  # 提取演员表
    regex5 = r'.*?releasetime.*?>(.*?)</p>'  # 提取上映时间
    regex6 = r'.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>'  # 提取评分
    pattern = re.compile(regex1 + regex2 + regex3 + regex4 + regex5 + regex6, re.S)  # 构建正则表达式
    results = re.findall(pattern, html)  # 匹配
    for result in results:
        yield {  # 使用生成器构建字典，结构化数据
            'index': result[0],
            # 'image': result[1],
            'title': result[2].strip(),
            'actor': result[3].strip()[3:] if len(result[3]) > 3 else '',
            'time': result[4].strip()[5:] if len(result[4]) > 5 else '',
            'score': result[5].strip() + result[6].strip()
        }


def write_to_file(content):  # 写入文件
    with open('result.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))  # 使用JSON库的dumps()方法实现字典的序列化，类型为字符串类型
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # ensure_ascii参数设为False，可以保证输出结果为中文形式，而不是Unicode编码


def main(offset):  # 将功能函数整合到主程序中，主程序提供接口
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
        time.sleep(1)  # 延时等待，防止爬取过快会无响应（猫眼反爬虫）
