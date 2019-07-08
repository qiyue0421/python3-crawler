# pyquery解析库的基本用法
# 优点为CSS选择器功能强大
from pyquery import PyQuery as pq

html = '''
<div id="container">
<ul class="list">
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''

"""初始化：需要传入HTML文本来初始化一个PyQuery对象
# 字符串初始化
doc = pq(html)  # 初始化一个PyQuery对象
print(doc('li'))  # 再传入CSS选择器

# url初始化
doc = pq(url='https://cuiqingcai.com')
print(doc('title'))

# 文件初始化
# doc = pq(filename='demo.html')
"""


"""基本CSS选择器
doc = pq(html)
print(doc('#container .list li'))  # 先选取id为container的节点，再选择其内部的class为list的节点内部的所有li节点
print(type(doc('#container .list li')))
"""


"""查找节点
# 查找子节点——find()方法
doc = pq(html)
items = doc('.list')  # 选取class为list的节点
print(type(items))
print(items)
lis = items.find('li')  # 选取内部的li节点
print(type(lis))
print(lis)

# 查找父节点——parent()方法
parent = items.parent()
print(parent)
print()

# 查找祖先节点——parents()方法
parents = items.parents()
print(parents)
print()

# 查找兄弟节点——siblings()方法
li = doc('.list .item-0.active')  # 首先选择class为list的节点内部class为item-0和active的节点
print(li.siblings())  # 找出它的兄弟节点
print(li.siblings('.active'))  # 传入css选择器，筛选特定的节点
"""


"""遍历
# 对于多个节点的结果，需要遍历获取
doc = pq(html)
lis = doc('li').items()  # 调用items()方法，获得一个生成器
print(type(lis))
for li in lis:
    print(li, type(li))
"""


"""获取信息
# 获取属性
doc = pq(html)
a = doc('.item-0.active a')
print(a, type(a))
print(a.attr('href'))  # 使用attr()方法获取属性
print(a.attr.href)  # 也可以通过调用attr属性来获取
print()

a = doc('a')  # 在属性获取阶段，需要观察返回节点是一个还是多个，如果是多个，则需要遍历才能依次获取每个节点的属性
for item in a.items():
    print(item.attr('href'))
print()

# 获取文本
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.text())  # 调用text()方法获取内部文本信息，忽略节点内部包含的所有HTML，只返回纯文字内容；如果是多个节点不需要遍历
print(a.html())  # 调用html()方法获取节点内部的HTML文本；如果是多个节点需要遍历
"""


"""节点操作
# addClass 和 removeClass——动态改变节点的class属性
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.remove_class('active')  # 移除active这个class
print(li)
li.add_class('active')  # 添加active这个class
print(li)

# attr、text和html
li.attr('name', 'link')  # 如果传入一个参数就是获取属性值，传入两个参数可以修改属性
print(li)
li.text('changed item')  # 如果传入参数就会改变节点内部内容
print(li)
li.html('<span>changed item</span>')  # 如果传入参数就会改变节点内部内容
print(li)

# remove()
string = '''
<div class="wrap">
Hello world
<p>This is a paragraph.</p>
</div>
'''
doc = pq(string)  # 只需要提取Hello world
print(doc('.wrap').text())  # 但是text()方法会获取所有纯文本内容组合成一个字符串

wrap = doc('.wrap')
wrap.find('p').remove()  # 选中p节点，调用remove()方法移除
print(wrap.text())
"""


"""伪类选择器
doc = pq(html)
li = doc('li:first-child')  # 第一个节点
print(li)
li = doc('li:last-child')  # 最后一个节点
print(li)
li = doc('li:nth-child(2)')  # 第二个节点
print(li)
li = doc('li:gt(2)')  # 第三个li后的节点（0为第一个节点）
print(li)
li = doc('li:nth-child(2n)')  # 偶数位置节点
print(li)
li = doc('li:contains(second)')  # 包含second文本的节点
print(li)
"""
