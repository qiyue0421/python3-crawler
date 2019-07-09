# 数据存储
from pyquery import PyQuery as pq
import requests
import json
import csv


"""文件存储"""
# 常见的文本形式为TXT、JSON、CSV等
"""TXT文本存储
# TXT文本几乎兼容任何平台，但是不利于检索数据
url = 'https://www.zhihu.com/explore'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
html = requests.get(url, headers=headers).text  # 获取网站源代码
doc = pq(html)
items = doc('.explore-tab .feed-item').items()  # 解析库解析，使用items()方法遍历获取多个节点
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()
    with open('explore.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join([question, author, answer]))
        f.write('\n' + '=' * 50 + '\n')
"""


"""JSON文件存储"""
# JSON，全称为JavaScript Object Notation，也就是JavaScript对象标记，它通过对象和数组的组合来表示数据，构造简洁但是结构化程度非常高，是一种轻量级的数据交换格式
# 对象：在JavaScript中是使用花括号{}包裹起来的内容，数据结构为{key1: value1, key2: value2, ...}的键值对结构
# 数组：在JavaScript中是方括号[]包裹起来的内容，数据结构为['java', 'javascript', 'vb', ...]的索引结构
# 一个JSON对象可以写为如下形式（特别注意，JSON数据必须使用双引号来包围，不能使用单引号，否则loads()方法会解析失败）：
'''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''
# JSON可以由以上两种形式自由组合而成，可以无限嵌套，结构清晰，是数据交换的极佳方式

"""读取JSON
string = '''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''
print(type(string))
data = json.loads(string)  # loads()方法将字符串转为JSON对象
print(data)
print(type(data))

print(data[0]['name'])  # 通过使用索引获取对应内容
print(data[0].get('name'))  # 使用get()方法传入键名，如果键名不存在，则不会报错，会返回None；支持传入第二个参数——默认值。
"""


"""输出JSON
data = [{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}]
with open('data.json', 'w') as f:
    f.write(json.dumps(data, indent=2))  # 使用dumps()方法将JSON对象转化为字符串，写入文本；参数indent表示缩进字符个数，传入该参数可以保存JSON的格式

data1 = [{
    "name": "王伟",
    "gender": "男",
    "birthday": "1992-10-18"
}]
with open('data.json', 'w', encoding='utf-8') as f:  # 规定文件输出编码为utf-8
    f.write(json.dumps(data1, indent=2, ensure_ascii=False))  # 指定参数ensure_ascii为False，可以输出中文
"""


"""CSV文件存储
# CSV全称为Comma-Separated Values，中文叫做逗号分割值或字符分割值，其文件以纯文本形式存储表格数据。
# 写入
with open('data.csv', 'w', newline='') as f:  # 加入newline参数，解决写入一行数据后会有空行的问题
    writer = csv.writer(f, delimiter=' ')  # writer()方法初始化写入对象，传入delimiter参数修改列与列之间的分割符
    writer.writerow(['id', 'name', 'age'])  # writerow()方法传入一行的数据
    writer.writerow(['10001', 'Mike', 20])
    writer.writerow(['10002', 'Bob', 22])
    writer.writerow(['10003', 'Jordon', 21])
    # writer.writerows([['10001', 'Mike', 20], ['10002', 'Bob', 22], ['10003', 'Jordon', 21]])  # 调用writerows()方法同时写入多行，此处参数需要为二维列表

# 字典写入
with open('data.csv', 'a', newline='') as f:
    filenames = ['id', 'name', 'age']  # 定义三个字段
    writer = csv.DictWriter(f, fieldnames=filenames)  # 初始化字典写入对象
    writer.writeheader()  # 写入头信息
    writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': 22})
    writer.writerow({'id': '10003', 'name': 'Jordon', 'age': 21})

# 写入中文
with open('data.csv', 'a', encoding='utf-8', newline='') as f:
    filenames = ['id', 'name', 'age']
    writer = csv.DictWriter(f, fieldnames=filenames)
    writer.writerow({'id': '10005', 'name': '王伟', 'age': 22})

# 读取
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
"""
