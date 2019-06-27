# 正则表达式的基本用法
import re


"""match()  # 传入要匹配的字符串以及正则表达式，检测正则表达式是否匹配字符串
# match()会从字符串的起始位置匹配正则表达式，一旦开头不匹配，那么整个匹配就失败，返回None
content = 'Hello 123 4567 World_This is a Regex Demo'
print(len(content))
result = re.match(r'^Hello\s\d{3}\s\d{4}\s\w{10}', content)  # 第一个参数传入正则表达式，第二个参数传入了要匹配的字符串
print(result)
print(result.group())  # group()方法输出匹配到的内容
print(result.span())  # span()方法输出匹配的范围
"""


"""匹配目标——从字符串中提取一部分内容
content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match(r'^Hello\s(\d+)\sWorld', content)  # 使用()括号将想要提取的子字符串括起来，()实际上标记了一个子表达式的开始和结束位置，被标记的每个子表达式会依次对应每个分组
print(result)
print(result.group(), result.span())
print(result.group(1), result.span(1))  # 在group()方法中传入分组的索引即可获取提取的结果
"""


"""通用匹配——.*
content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match(r'^Hello.*Demo', content)  # 万能匹配.*，.（点）可以匹配任意字符（除了换行符）,*（星号）代表匹配前面的字符无限次，组合在一起可以匹配任意字符
print(result)
print(result.group(), result.span())
"""


"""贪婪与非贪婪
content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match(r'^He.*(\d+).*Demo$', content)  # 在贪婪模式下，.*会尽可能匹配多的字符
print(result)
print(result.group(1))  # .*的贪婪模式将123456匹配了，只给\d+留下一个可满足条件的数字7

result1 = re.match(r'He.*?(\d+).*Demo$', content)  # 在.*后面加入？(问号），启用非贪婪匹配，尽可能匹配少的字符
print(result1)
print(result1.group(1))  # 在贪婪模式下，\d+可以匹配到1234567
"""


"""修饰符
# 正则表达式可以包含一些可选标志修饰符来控制匹配的模式
content = "Hello 1234567 World_This \n is a Regex Demo"
result = re.match(r'^He.*?(\d+).*?Demo$', content, re.S)  # re.S修饰符的作用是使.（点号）匹配包括换行符在内的所有字符
print(result.group(1))
# re.I  忽略大小写
# re.L  做本地化识别匹配
# re.M  多行匹配，影响^和$
# re.S  使.匹配包括换行符在内的所有字符
# re.U  根据Unicode字符集解析字符
# re.X  允许使用“#”引导注释
"""


"""转义匹配
content = '(百度)www.baidu.com'
result = re.match('\(百度\)www\.baidu\.com', content)  # 遇到特殊字符时，在前面加反斜线转义即可
print(result.group())
"""


"""search()"""
#





