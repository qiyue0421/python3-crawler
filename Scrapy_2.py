"""3、Selector的用法"""
# Scrapy提供了自己的数据提取方法，即Selector（选择器），Selector是基于lxml来构建的，支持XPath选择器、CSS选择器以及正则表达式，功能全面，解析速度和准确度非常高

"""直接使用
# Selector是一个可以独立使用的模块，可以直接用Selector类来构建一个选择器对象，然后调用它的相关方法如xpath()、css()等来提取数据
# 例如，针对一段HTML代码，可以使用如下方式构建Selector对象来提取数据：

from scrapy import Selector

body = '<html><head><title>Hello World</title></head><body>Qiyue</body></html>'
selecot = Selector(text=body)  # 构建时传入text参数，生成一个Selector选择器对象
title = selecot.xpath('//body/text()').extract_first()  # 调用xpath()方法提取信息
print(title)

"""


"""Scrapy shell
# 借助Scrapy shell来模拟Scrapy请求过程，样例页面为官方文档：http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
# 开启Scrapy shell，在命令行下输入命令：
# scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
# 这样就进入了shell模式，这个过程其实是：Scrapy发起了一次请求，请求的URL就是命令行输入的URL，然后把一些可操作的变量传递给我们，如request、response等
#
# 页面源码如下：

<html>
<head>
  <base href="http://example.com/">
  <title>Example website</title>
</head>
<body>
<div id="images">
<a href="image1.html"> Name: My image 1 <br /><img src="image1_thumb.jpg" /></a>
<a href="image2.html"> Name: My image 2 <br /><img src="image2_thumb.jpg" /></a>
<a href="image3.html"> Name: My image 3 <br /><img src="image3_thumb.jpg" /></a>
<a href="image4.html"> Name: My image 4 <br /><img src="image4_thumb.jpg" /></a>
<a href="image5.html"> Name: My image 5 <br /><img src="image5_thumb.jpg" /></a>
</div>
</body>
</html>

"""


"""XPath选择器
# 进入shell模式后，我们主要操作response变量进行解析，因为我们解析的是HTML代码，Selector将自动使用HTML语法来分析。response有一个属性selector，
# 调用response.selector返回的内容就相当于用response的text构造了一个Selector对象，通过这个Selector对象我们可以调用解析方法如xpath()、css()等，通过向方法传入XPath或CSS选择器参数就可以实现信息的提取

>>> result = response.selector.xpath('//a')
>>> result
[<Selector xpath='//a' data='<a href="image1.html">Name: My image 1 <'>, 
<Selector xpath='//a' data='<a href="image2.html">Name: My image 2 <'>, 
<Selector xpath='//a' data='<a href="image3.html">Name: My image 3 <'>, 
<Selector xpath='//a' data='<a href="image4.html">Name: My image 4 <'>,
<Selector xpath='//a' data='<a href="image5.html">Name: My image 5 <'>]
>>> type(result)
<class 'scrapy.selector.unified.SelectorList'>

# 打印结果的形式是Selector组成的列表，其实它是SelectorList类型，SelectorList和Selector都可以继续调用xpath()和css()等方法进一步提取数据
# 上面我们提取了 a 节点，接下来，尝试调用xpath()方法提取 a 节点内包含的 img 节点，如下：

>>> result.xpath('./img')  # 注意此处选择器的最前方加 .(点)，这代表提取元素内部的数据，没有加点表示从根节点开始提取
[<Selector xpath='./img' data='<img src="image1_thumb.jpg">'>, 
<Selector xpath='./img' data='<img src="image2_thumb.jpg">'>, 
<Selector xpath='./img' data='<img src="image3_thumb.jpg">'>, 
<Selector xpath='./img' data='<img src="image4_thumb.jpg">'>, 
<Selector xpath='./img' data='<img src="image5_thumb.jpg">'>]

# Scrapy提供了两个实用的快捷方法，response.xpath()和response.css()，它们二者的功能完全等于response.selector.xpath()和response.selector.css()
# 
# 现在我们得到的是SelectorList类型的变量，该变量由Selector对象组成的列表，
# ①、可以使用索引单独取出某个Selector元素，如下所示：

>>> result[0]
<Selector xpath='//a' data='<a href="image1.html">Name: My image 1 <'>

# ②、可以使用extract()方法提取节点的文本内容，如下所示：

>>> result.extract()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', 
'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>', 
'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>', 
'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>', 
'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

# ③、可以改写XPath表达式，来选取节点的内部文本和属性，如下所示：

>>> response.xpath('//a/text()').extract()  # 加一层 /text() 就可以获取节点的内部文本
['Name: My image 1 ', 'Name: My image 2 ', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
>>> response.xpath('//a/@href').extract()  # 加一层 /@href 就可以获取节点的href属性，其中，@符号后面内容就是要获取的属性名称
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

# ④、可以使用extract_first()方法将匹配的第一个结果提取出来，也可以为extract_first()方法设置一个默认值参数，这样当XPath规则提取不到内容时会直接使用默认值

>>> response.xpath('//a[@href="image1.html"]/text()').extract_first()
['Name: My image 1 ']
>>> response.xpath('//a[@href="image1"]/text()').extract_first()  # 这里如果XPath匹配不到任何元素，返回空，也不会报错
>>> response.xpath('//a[@href="image1"]/text()').extract_first('Default Image')  # 主动设置一个默认值参数
'Default Image'

"""


"""CSS选择器
# Scrapy的选择器同时对接了CSS选择器，使用response.css()方法可以使用CSS选择器来选择对应的元素，例如上文选取所有的 a 节点，CSS选择器同样可以做到：

>>> response.css('a')
[<Selector xpath='descendant-or-self::a' data='<a href="image1.html">Name: My image 1 <'>, 
<Selector xpath='descendant-or-self::a' data='<a href="image2.html">Name: My image 2 <'>, 
<Selector xpath='descendant-or-self::a' data='<a href="image3.html">Name: My image 3 <'>, 
<Selector xpath='descendant-or-self::a' data='<a href="image4.html">Name: My image 4 <'>, 
<Selector xpath='descendant-or-self::a' data='<a href="image5.html">Name: My image 5 <'>]

# ①、调用extract()方法可以提取出节点中的文本内容，如下所示：

>>> response.css('a').extract()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', 
'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>', 
'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>', 
'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>', 
'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

# ②、另外，可以进行属性选择和嵌套选择，如下所示：

>>> response.css('a[href="image1.html"]').extract()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>']
>>> response.css('a[href="image1.html"] img').extract()
['<img src="image1_thumb.jpg">']

# ③、也可以使用extract_first()方法提取列表的第一个元素，如下所示：

>>> response.css('a[href="image1.html"] img').extract_first()
'<img src="image1_thumb.jpg">'

# ④、节点内部文本和属性的获取需要用 ::text() 和 ::attr() 的写法，如下所示：

>>> response.css('a[href="image1.html"]::text').extract_first()
'Name: My image 1 '
>>> response.css('a[href="image1.html"] img::attr(src)').extract_first()
'image1_thumb.jpg'

# ⑤、CSS选择器和XPath选择器一样可以嵌套选择，我们可以先用XPath选择器选中所有 a 节点，再利用CSS选择器选中 img 节点，再用XPath选择器获取属性，如下所示：

>>> response.xpath('//a').css('img').xpath('@src').extract()  # 随意使用css()和xpath()方法二者自由组合实现嵌套查询，完全兼容
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']

"""


"""正则匹配
# Scrapy的选择器还支持正则匹配
# ①、比如，在示例的 a 节点中的文本类似于 Name: My image 1，现在我们只想要把 Name: 后面的内容提取出来，可以借助re()方法，如下所示：

>>> response.xpath('//a/text()').re('Name:\s(.*)')  # 给re()方法传了一个正则表达式，其中(.*)就是要匹配的内容，输出的结果就是正则表达式匹配的分组，结果会依次输出
['My image 1 ', 'My image 2 ', 'My image 3 ', 'My image 4 ', 'My image 5 ']

# ②、如果同时存在两个分组，那么结果依然会按序输出，如下所示：

>>> response.xpath('//a/text()').re('(.*):\s(.*)')
['Name', 'My image 1 ', 'Name', 'My image 2 ', 'Name', 'My image 3 ', 'Name', 'My image 4 ', 'Name', 'My image 5 ']

# ③、类似extract_first()方法，re_first()方法可以选取列表的第一个元素，如下所示：

>>> response.xpath('//a/text()').re_first('(.*):\s(.*)')
'Name'
>>> response.xpath('//a/text()').re_first('Name:\s(.*)')
'My image 1 '

# ④、需要注意的是，response对象不能直接调用re()和re_first()方法。如果想要对全文进行正则匹配，可以先调用xpath()方法再进行正则匹配，如下所示：

>>> response.re('Name:\s(.*)')
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'HtmlResponse' object has no attribute 're'
>>> response.xpath('.').re('Name:\s(.*)<br>')  # 这里使用xpath('.')选中全文
['My image 1 ', 'My image 2 ', 'My image 3 ', 'My image 4 ', 'My image 5 ']
>>> response.xpath('.').re_first('Name:\s(.*)<br>')
'My image 1 '

"""
