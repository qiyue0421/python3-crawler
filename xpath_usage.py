# XPath,全称XML Path Language,即XML路径语言，是一门在XML文档中查找信息的语言
# 使用前需要安装lxml库

# XPath常用规则
# 表达式    描述
# nodename  选取此节点的所有子节点
# /         从当前节点选取直接子节点
# //        从当前节点选取子孙节点
# .         选取当前节点
# ..        选取当前节点的父节点
# @         选取属性

# 例如：
# //title[@lang='eng']
# 选取所有名称为title，同时属性lang的值为eng的节点

from lxml.html import etree


"""XPath对网页的解析过程
text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
</ul>
</div>
'''
html = etree.HTML(text)  # 构造一个XPath解析对象，注意text中最后一个<li>节点没有闭合，但是etree模块会自动修正HTML文本
result = etree.tostring(html)  # 输出修正后的结果，类型为bytes
print(result.decode('utf-8'))  # 转为str类型
"""


"""读取文本文件进行解析
html = etree.parse('./text.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))
"""


"""使用规则选取符合要求的节点
html = etree.parse('./text.html', etree.HTMLParser())
result = html.xpath('//*')  # 使用//选取所有符合要求的节点，使用*匹配所有节点
result1 = html.xpath('//li')  # 选取所有li节点
print(result)  # 返回一个列表，其中的每个元素为Element类型，显示节点名称
print(result1)
'''[<Element html at 0x1eeeff5f408>, <Element body at 0x1eeeff5f3c8>, <Element div at 0x1eeeff5f488>, <Element ul at 0x1eeeff5f4c8>, <Element li at 0x1eeeff5f508>, 
<Element a at 0x1eeeff5f588>, <Element li at 0x1eeeff5f5c8>, <Element a at 0x1eeeff5f608>, <Element li at 0x1eeeff5f648>, <Element a at 0x1eeeff5f548>, <Element li at 0x1eeeff5f688>, 
<Element a at 0x1eeeff5f6c8>, <Element li at 0x1eeeff5f708>, <Element a at 0x1eeeff5f748>]'''
"""


"""查找子节点、子孙节点及父节点
html = etree.parse('./text.html', etree.HTMLParser())
result = html.xpath('//li/a')  # 使用/查找当前节点的子节点
result1 = html.xpath('//li//a')  # 使用//查找当前节点的子孙节点
result2 = html.xpath('//a[@href="link4.html"]/../@class')  # 使用..查找当前节点的父节点
# result2 = html.xpath('//a[@href="link4.html"]/parent::*/@class')  # 也可以使用parent::获取父节点
print(result)
print(result1)
print(result2)
"""


"""属性匹配与属性获取
html = etree.parse('./text.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]')  # 使用[]和@符号匹配属性，此处限定节点的class属性为"item-0"
result1 = html.xpath('//li/a/@href')  # 单独获取节点属性直接使用@，返回属性值列表
print(result)
print(result1)
"""


"""节点文本获取——text()方法
html = etree.parse('./text.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/a/text()')  # <a>节点是<li>的子节点，要想获取<li>节点内部的文本，可以逐层选取
result1 = html.xpath('//li[@class="item-0"]//text()')  # 直接使用//选取<li>节点的所有子孙节点，返回三个结果，前两个是<a>节点内部的文本，第三个是最后一个<li>节点内部的文本，即换行符
print(result)
print(result1)
# 输出为：
# ['first item', 'fifth item']
# ['first item', 'fifth item', '\r\n']
"""


"""属性多值匹配——某个属性可能有多个值
text = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)  # 文本中class属性有两个值li和li-first
result = html.xpath('//li[contains(@class, "li")]/a/text()')  # 使用contains()方法，第一个参数传入属性名，第二个参数传入属性值
print(result)
"""


"""多属性匹配——节点有多个属性
text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')  # 使用运算符and连接多个属性
print(result)
"""


"""按序选择——选择某个节点
html = etree.parse('./text.html', etree.HTMLParser())
result = html.xpath('//li[1]/a/text()')  # 第一个节点
print(result)
result = html.xpath('//li[last()]/a/text()')  # 最后一个节点
print(result)
result = html.xpath('//li[position()<3]/a/text()')  # 位置小于3的节点，即第一个、第二个节点
print(result)
result = html.xpath('//li[last()-2]/a/text()')  # 倒数第三个节点，last()是倒数第一，last()-2即倒数第三个
print(result)
# 输出为：
# ['first item']
# ['fifth item']
# ['first item', 'second item']
# ['third item']
"""


"""节点轴选择
# XPath提供了很多节点轴选择方法，包括获取子元素、兄弟元素、父元素、祖先元素等
text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html"><span>first item</span></a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
</ul>
</div>
'''
html = etree.HTML(text)
result = html.xpath('//li[1]/ancestor::*')  # 调用ancestor轴，可以获取所有祖先节点，其后需要跟两个冒号::
print(result)
result = html.xpath('//li[1]/ancestor::div')  # 在冒号后面加div，限定祖先节点为div
print(result)
result = html.xpath('//li[1]/attribute::*')  # 调用attribute轴，可以获取所有属性值
print(result)
result = html.xpath('//li[1]/child::a[@href="link1.html"]')  # 调用child轴，可以获取所有直接子节点，后面接了限定条件
print(result)
result = html.xpath('//li[1]/descendant::span')  # 调用descendant轴，获取所有子孙节点，限定条件为span
print(result)
result = html.xpath('//li[1]/following::*[2]')  # 调用following轴，可以获取当前节点之后的所有节点，使用索引[2]获取第二个后续节点
print(result)
result = html.xpath('//li[1]/following-sibling::*')  # 调用following-sibling轴，可以获取当前节点之后的所有同级节点
print(result)
# 输出为：
# [<Element html at 0x1f2a01bedc8>, <Element body at 0x1f2a05505c8>, <Element div at 0x1f2a0550488>, <Element ul at 0x1f2a0550548>]
# [<Element div at 0x1f2a0550488>]
# ['item-0']
# [<Element a at 0x1f2a0550548>]
# [<Element span at 0x1f2a0550488>]
# [<Element a at 0x1f2a0550548>]
# [<Element li at 0x1f2a05505c8>, <Element li at 0x1f2a0550648>, <Element li at 0x1f2a0550688>, <Element li at 0x1f2a05506c8>]
"""
