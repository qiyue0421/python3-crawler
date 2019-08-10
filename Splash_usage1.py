# Splash是一个JavaScript渲染服务，是一个带有HTTP API的轻量级浏览器，同时它对接了Python中的Twisted和QT库，利用它可以实现动态渲染页面的抓取。

"""1、功能介绍
# Splash功能：
# 异步方式处理多个网页渲染过程；
# 获取渲染后的页面的源代码或截图；
# 通过关闭图片渲染或者使用Adblock规则来加快页面渲染速度；
# 可执行特定的JavaScript脚本；
# 可通过Lua脚本来控制页面渲染过程；
# 获取渲染的详细过程并通过HAR（HTTP Archive）格式呈现。
"""


"""2、准备工作

# Docker安装教程
# https://www.runoob.com/docker/windows-docker-install.html
# （Docker Desktop for Windows桌面应用程序 https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe）
# 安装Splash
# docker run -p 8050:8050 scrapinghub/splash
"""


"""3、实例引入
# 打开http://localhost:8050/即可看到Splash服务的Web页面
"""


"""4、Splash Lua脚本"""
# Splash可以通过Lua脚本执行一系列渲染操作，这样就可以模拟类似Chrome、PhantomJS的操作、
# Lua脚本示例：
# function main(splash, args)
#   assert(splash:go(args.url))  # 调用go()方法加载页面
#   assert(splash:wait(0.5))  # 调用wait()方法等待一定时间
#   return {
#     html = splash:html(),  # 返回页面源码
#     png = splash:png(),  # 返回截图
#     har = splash:har(),  # 返回HAR信息
#   }
# end

"""入口及返回值
# 首先，来看一个基本实例：
# function main(splash, args)  # main()方法名字是固定的，Splash会默认调用这个方法，返回值既可以是字典形式，也可以是字符串形式
#     splash:go("http://www.baidu.com")
#     splash:wait(0.5)
#     local title = splash:evaljs("document.title")  # evaljs()方法传入JavaScript脚本，而document.title的执行结果就是返回页面标题
#     return {title=title}  # 返回的是字典形式
# end

# 将上述代码粘贴到web页面上，测试发现它返回了网页的标题
"""


"""异步处理
# Splash支持异步处理，但是这里并没有显式指明回调方法，其回调的跳转是在Splash内部完成的
# 示例如下：
# function main(splash, args)
#     local example_urls = {"www.baidu.com", "www.taobao.com", "www.zhihu.com"}
#     local urls = args.urls or example_urls
#     local results = {}
#     for index, url in ipairs(urls) do
#         local ok, reason = splash:go("http://" .. url)  # 注意此处，Lua脚本使用符号..作为连接操作符
#         if ok then
#             splash:wait(2)  # wait()方法类似于python中的sleep()，当Splash执行到此方法时，它会转而去处理其他任务，然后在指定的时间过后再回来继续处理
#             results[url] = splash:png()
#         end
#     end
#     return results
# end

# 运行结果是3个不同站点的截图
"""


"""5、Splash对象属性"""
# main()方法的第一个参数是splash，这个对象类似于Selenium中的WebDriver对象，可以调用它的一些属性和方法来控制加载加载过程

"""args
# 该属性可以获取加载时配置的参数，比如URL，如果为GET请求，它还可以获取GET请求参数；如果为POST请求，它可以获取表单提交的数据
# function main(splash, args)  # args参数相当于splash.args属性
#     local url = args.url
# end
#
# 以上代码等价于
# function main(splash)
#     local url = splash.args.url
# end
"""


"""js_enabled
# 这个属性是Splash的JavaScript执行开关，可以将其配置为true或false来控制是否执行JavaScript代码，默认为true。
# 我们尝试禁止执行JavaScript代码，运行结果会抛出异常
# function main(splash, args)
#     splash:go("http://www.baidu.com")
#     splash.js_enabled = false
#     local title = splash:evaljs("document.title")
#     return {title=title}
# end
"""


"""resource_timeout
# 此属性可以设置加载的超时时间，单位是秒。如果设置为0或nil（类似python中的None），代表不检测超时。
# function main(splash)
#     splash.resource_timeout = 0.1  # 设置等待时间为0.1秒，如果期间没有得到响应，就会抛出异常
#     assert(splash:go('https://www.taobao.com'))
#     return splash:png()
# end
"""


"""images_enabled
# 此属性可以设置图片是否加载，默认情况下是加载的，禁用该属性后，可以节省网络流量并提高网页加载速度。
# 但是需要注意的，禁用图片加载可能会影响到JavaScript渲染，因为禁用后它的外层DOM节点的高度会受影响，进而影响DOM节点的位置。
# function main(splash, args)
#     splash.images_enabled = false
#     assert(splash:go('https://www.jd.com'))
#     return {png=splash.png()}
# end
"""


"""plugins_enabled
# 此属性可以控制浏览器插件（比如Flash插件）是否开启。默认情况下，此属性为false，表示不开启
# splash.plugins_enabled = true/false  # 控制开启和关闭
"""


"""scroll_position
# 通过设置此属性，我们可以控制页面上下或左右滚动，比较常用
# function main(splash, args)
#     assert(splash:go('https://www.taobao.com'))
#     splash.scroll_position = {y=400}  # 控制页面向下滚动400像素值
#     return {png=splash:png()}
# end

# 如果要让页面左右滚动，可以传入x参数
# splash.scroll_position = {x=100, y=200
"""
