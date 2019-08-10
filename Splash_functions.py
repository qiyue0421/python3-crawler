"""6、Splash对象的方法"""
"""go()
# 该方法用来请求某个链接，而且它可以模拟GET和POST请求，同时支持传入请求头、表单等数据
#
# 用法：
# ok, reason = splash:go{url, baseurl=nil, headers=nil, http_method="GET", body=nil, formdata=nil}
#
# 参数说明：
# nul：请求的URL
# baseurl：可选参数，默认为空，表示资源加载相对路径
# headers：可选参数，默认为空，表示请求头
# http_method：可选参数，默认为GET，同时支持POST
# body：可选参数，默认为空，发POST请求时的表单数据，使用的Content-type为application/json
# formdata：可选参数，默认为空，发POST的时候的表单数据，使用的Content-type为application/x-www-form-urlencoded
#
# 该方法返回的结果是结果ok和原因reason的组合，如果ok为空，代表网页加载出现了错误，此时reason变量中包含了错误的原因，否则证明页面加载成功
# 示例：
# function main(splash, args)
#     local ok, reason = splash:go{"http://httpbin.org/post", http_method="POST", body="name=Germey"}  # 模拟了一个POST请求，并传入了POST表单数据
#     if ok then
#         return splash:html()  # 如果加载成功吗，则返回页面源代码
#     end
# end
"""


"""wait()
# 此方法可以控制页面的等待时间
#
# 用法：
# ok, reason = splash:wait{time, cancel_on_redirect=false, cancel_on_error=true}
#
# 参数说明：
# time：等待的秒数
# cancel_on_redirect：可选参数，默认为false，如果为true，表示如果发生了重定向就停止等待，并返回重定向结果
# cancel_on_error：可选参数，默认为true，表示如果发生了加载错误，就停止等待
#
# 该方法返回的结果是结果ok和原因reason的组合
# 示例：
# function main(splash)
#     splash:go("https://www.taobao.com")
#     splash:wait(2)  # 等待2秒
#     return {html=splash:html()}
# end
"""


"""jsfunc()
# 此方法可以直接调用JavaScript定义的方法，但是所调用的方法需要用双中括号包围，这相当于实现了JavaScript方法到Lua脚本的转换
#
# 示例：
# function main(splash, args)
#     local get_div_count = splash:jsfunc([[  # 计算页面中div节点的个数
#     function(){
#         var body = document.body;
#         var divs = body.getElementsByTagName('div');
#         return divs.length;
#     }
#     ]])
#     splash:go("https://www.baidu.com")
#     return ("These are %s DIVs"):format(get_div_count())
# end
"""


"""evaljs()
# 此方法可以执行JavaScript代码并返回最后一条JavaScript语句的返回结果
#
# 用法：
# result = splash:evaljs(js)
#
# 示例：
# local title = splash:evaljs("document.title")
"""


"""runjs()
# 此方法可以执行JavaScript代码，它与evaljs()的功能类似，但是偏向于执行某些动作或声明某些方法
#
# 示例：
# function main(splash, args)
#     splash:go("https://www.baidu.com")
#     splash:runjs("foo = function(){return 'bar'}")  # runjs()声明JavaScript定义的方法
#     local result = splash:evaljs("foo()")  # evaljs()调用方法
#     return result
# end
"""


"""autoload()
# 此方法可以设置每个页面访问时自动加载的对象，但是该方法只负责加载JavaScript代码或库，不执行任何操作
#
# 用法
# ok, reason = splash:autoload{source_or_url, source=nil, url=nil}
#
# 参数说明
# source_or_url：JavaScript代码或者JavaScript库链接
# source：JavaScript代码
# url：JavaScript库链接
#
# 示例：
# function main(splash, args)
#     splash:autoload([[  # 声明方法
#         function get_document_title(){
#             return document.title;
#         }
#     ]])
#     splash:go("https://www.baidu.com")
#     return splash:evaljs("get_document_title()")  # 调用执行方法
# end
"""


"""call_later()
# 此方法可以通过设置定时任务和延迟时间来实现任务延时执行，并且可以在执行前通过cancel()方法重新执行定时任务
#
# 示例：
# function main(splash, args)
#     local snapshots = {}
#     local timer = splash:call_later(function()  # 设置定时任务
#         snapshots["a"] = splash:png()  # 0.2秒时获取网页截图，此时网页还没有加载出来，截图为空
#         splash:wait(1.0)  # 等待1秒
#         snapshots["b"] = splash:png()  # 1.2秒时再次获取网页截图，此时网页加载成功
#     end, 0.2)
#     splash:go("https://www.baidu.com")
#     splash:wait(3.0)
#     return snapshots
# end
"""