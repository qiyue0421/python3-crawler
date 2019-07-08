# Beautiful Soup是python的一个HTML或XML解析库，善于提取数据
# 自动将输入文档转换为Unicode编码，输出文档转换为UTF-8编码
# 在解析时依赖解析库，除了支持python标准库中的HTML解析器外，还支持一些第三方解析器（lxml、html5lib）
from bs4 import BeautifulSoup
import re

html = '''
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three title sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
'''

string = '''
<div class="panel">
<div class="panel-heading">
<h4>hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1" name="elements">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jay</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
<p>link 1</p>
</ul>
</div>
</div>
'''

"""基本用法
soup = BeautifulSoup(html, 'lxml')  # BeautifulSoup对象初始化（自动更正格式），解析器为lxml
print(soup.prettify())  # prettify()方法将要解析的字符串以标准的缩进格式输出
print(soup.title.string)  # 输出title节点的文本内容
"""


"""节点选择器"""
"""选择元素
# 直接调用节点的名称就可以选择节点元素，再调用string属性就可以得到节点内的文本
soup = BeautifulSoup(html, 'lxml')
print(soup.title)
print(type(soup.title))
print(soup.title.string)
print(soup.head)
print(soup.p)  # 选择第一个匹配到的节点，后面节点会忽略
"""


"""提取信息
# 使用name属性获取节点的名称
soup = BeautifulSoup(html, 'lxml')
print(soup.title.name)

# 调用attrs获取所有属性
print(soup.p.attrs)  # 返回一个包含属性和属性值的字典

# 获取单独属性
print(soup.p.attrs['name'])  # 第一种方式相当于从字典中提取键值
print(soup.p['name'])  # 第二种方式直接在节点元素后面加中括号，传入属性名获取，因为是唯一属性，返回单个字符串
print(soup.p['class'])  # 因为属性值不唯一，所以返回的是一个列表
# 输出为
# dromouse
# dromouse
# ['title']

# 获取内容
print(soup.p.string)  # 利用string属性获取节点元素包含的文本内容
"""


"""嵌套选择
soup = BeautifulSoup(html, 'lxml')
print(soup.head.title)  # 嵌套调用选择节点
print(type(soup.head.title))  # 得到的结果依然是Tag类型
print(soup.head.title.string)
"""


"""关联选择
html1 = '''
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="story">
    Once upon a time there were three title sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
and they lived at the bottom of a well.
</p>
'''
# 子节点与孙节点
soup = BeautifulSoup(html1, 'lxml')
print(soup.p.contents)  # 调用contents属性获取节点元素的直接子节点，返回一个列表，其中每个元素都是p节点的直接子节点（不包含孙子节点）
print()
print(soup.p.children)  # 调用children属性可以得到一样的结果，返回一个生成器
for i, child in enumerate(soup.p.children):
    print(i)
    print(child)

print(soup.p.descendants)  # 递归查询，获取所有子孙节点
for i, child in enumerate(soup.p.descendants):
    print(i)
    print(child)

# 父节点和祖先节点
print(soup.a.parent)  # 获取a节点的父节点
print(soup.p.parents)  # 获取所有的祖先节点，返回结果是生成器类型
print()
print(list(enumerate(soup.p.parents)))

# 兄弟节点
print('next sibling', soup.a.next_sibling)  # 下一个兄弟节点
print('prev sibling', soup.a.previous_sibling)  # 上一个兄弟节点
print('next siblings', list(enumerate(soup.a.next_siblings)))  # 后面的兄弟节点
print('prev siblings', list(enumerate(soup.a.previous_siblings)))  # 前面的兄弟节点
"""


"""方法选择器
# find_all(name, attrs, recursive, text, ***kwargs)——查询所有符合条件的元素

# name参数——节点名查询
soup = BeautifulSoup(string, 'lxml')
print(soup.find_all(name='ul'))  # 传入name参数，查询所有ul节点，返回一个列表
print(type(soup.find_all(name='ul')[0]))  # bs4.element.Tag类型

for ul in soup.find_all(name='ul'):  # 进行嵌套查询
    print(ul.find_all(name='li'))  # 获取内部li节点
    for li in ul.find_all(name='li'):  # 遍历每个li
        print(li.string)  # 获取文本信息

# attrs参数——属性查询
print(soup.find_all(attrs={'id': 'list-1'}))  # 传入的参数为字典类型，返回结果为列表
print(soup.find_all(attrs={'name': 'elements'}))

print(soup.find_all(id='list-1'))  # 或者直接传入参数
print(soup.find_all(class_='element'))

# text参数——匹配节点文本，传入形式可以是字符串或者正则表达式对象
print(soup.find_all(text=re.compile('link')))


# find(name, attrs, recursive, text, ***kwargs)——查询第一个符合条件的元素
soup = BeautifulSoup(string, 'lxml')
print(soup.find(name='ul'))
print(type(soup.find(name='ul')))
"""


"""CSS选择器
soup = BeautifulSoup(string, 'lxml')
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))  # 选择ul节点下面的所有li节点
print(soup.select('#list-2 .element'))
print(type(soup.select('ul')[0]))

# 嵌套选择
for ul in soup.select('ul'):
    print(ul.select('li'))
    print(ul['id'])  # 获取属性
    # print(ul.attrs['id'])

# 获取文本
for li in soup.select('li'):
    print('Get text:', li.get_text())
    # print('String:', li.string)
"""
