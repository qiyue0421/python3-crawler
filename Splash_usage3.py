import requests
from urllib.parse import quote

"""7、Splash API"""
# Splash提供了一些HTTP API接口，我们通过请求这些接口并传递相应的参数到python程序中，进行抓取JavaScript渲染的页面

"""render.html
# 此接口用于获取JavaScript渲染的页面的HTML代码，接口地址就是Splash的运行地址加此接口名称
# 例如 http://localhost:8050/render.html
#
# 使用curl测试
# curl http://localhost:8050/render.html?url=https://www.baidu.com
# 我们给此接口传递了一个url参数来指定渲染的URL，返回结果即页面渲染后的源代码
url = 'http://localhost:8050/render.html?url=https://www.baidu.com'
response = requests.get(url)
print(response.text)
"""


"""render.png
# 此接口可以获取网页截图，通过width和height来控制宽高，返回的是PNG格式的图片二进制数据
# curl http://localhost:8050/render.png?url=https://www.baidu.com&wait=5&width=1000&height=700
url = 'http://localhost:8050/render.png?url=https://www.taobao.com&wait=5&width=1000&height=700'
response = requests.get(url)
with open('taobao.png', 'wb') as f:
    f.write(response.content)
"""


"""render.jpeg
# 此接口与render.png类似，不过返回的是JPEG格式的图片二进制数据，此外，多了一个quality参数，用来控制设置图片质量
"""


"""render.har
# 此接口用于获取页面加载的HAR数据
# curl http://localhost:8050/render.har?url=https://www.baidu.com&wait=5
# 它返回的结果非常多，是一个JSON格式的数据，其中包含页面加载过程中的HAR数据
"""


"""render.json
# 此接口包含了前面接口的所有功能，返回结果是JSON格式
# curl http://localhost:8050/render.json?url=https://httpbin.org
#
# 结果如下:
# {"type": "GlobalTimeoutError", "info": {"timeout": 30}, "description": "Timeout exceeded rendering page", "error": 504}
# 以JSON形式返回了相应的请求数据
#
# 可以通过传入不同参数控制其返回结果：
# 传入html=1，返回结果即会增加源代码数据；
# 传入png=1，返回结果即会增加页面PNG截图数据；
# 传入har=1，则会获取页面HAR数据
# curl http://localhost:8050/render.json?url=https://httpbin.org&html=1&png=1&har=1
"""


"""execute
# 此接口才是最为强大的接口，可以实现与Lua脚本的对接
lua = '''
function main(splash)
    return 'hello'
end
'''

url = 'http://localhost:8050/execute?lua_source=' + quote(lua)  # 使用quote()方法进行URL转码
response = requests.get(url)
print(response.text)
"""


"""8、Splash负载均衡配置"""
# 使用Splash做页面抓取时，如果爬取的量非常大，任务非常多，用一个Splash服务来处理的话，未免压力太大了，
# 此时可以考虑搭建一个负载均衡器来把压力分散到各个服务器上。这相当于多台机器多个服务共同参与任务的处理，可以减小单个Splash服务的压力。

"""配置Splash服务
# 要搭建Splash负载均衡，首先要有多个Splash服务。
# 假设有四台远程主机，它们的8050端口上都开启了Splash服务，都是通过Docker的Splash镜像开启的，访问其中任何一个服务时，都可以使用Splash服务
# 主机地址：
# 41.159.27.223:8050
# 41.159.27.221:8050
# 41.159.27.9:8050
# 41.159.117.119:8050
# 接下来可以选用任意一台带有公网IP的主机来配置负载均衡
"""


"""配置负载均衡
# 首先，在主机上装好Nginx，然后修改Nginx的配置文件nginx.conf，添加以下内容：
# 通过upstream字段定义了一个名字叫做splash的服务集群配置
# 配置完后需要重启Nginx服务： nginx -s load
'''
# 最少链接负载均衡：它适合处理请求处理时间长短还不一造成服务器过载的情况
http {
    upstream splash {
        least_conn;
        server 41.159.27.223:8050;
        server 41.159.27.221:8050;
        server 41.159.27.9:8050;
        server 41.159.117.119:8050;
    }
    server {
        listen 8050;
        location / {
            proxy_pass http://splash;
        }
    }
}
'''

'''
# 轮询策略负载均衡：每个服务器的压力相同，此策略适合服务器配置相当，无状态且短平快的服务使用
upstream splash {
    server 41.159.27.223:8050;
    server 41.159.27.221:8050;
    server 41.159.27.9:8050;
    server 41.159.117.119:8050;
}
'''

'''
# 指定权重负载均衡：weight参数指定各个服务的权重，权重越高，分配到处理的请求越多，假如不同的服务器配置差别比较大的话，可以使用此种配置
upstream splash {
    server 41.159.27.223:8050 weight=4;
    server 41.159.27.221:8050 weight=2;
    server 41.159.27.9:8050 weight=2;
    server 41.159.117.119:8050 weight=1;
}
'''

'''
# IP散列负载均衡：服务器根据请求客户端的IP地址进行散列计算，确保使用同一服务器响应请求，这种策略适合有状态的服务，比如用户登录后访问某个页面的情形
upstream splash {
    ip_hash;
    server 41.159.27.223:8050;
    server 41.159.27.221:8050;
    server 41.159.27.9:8050;
    server 41.159.117.119:8050;
}
'''
"""


"""配置认证
# Splash可以公开访问，如果不想让其公开访问，还可以配置认证，同样借助于Nginx实现，在server的location字段中添加auth_basic和auth_basic_user_file字段
'''
http {
    upstream splash {
        least_conn;
        server 41.159.27.223:8050;
        server 41.159.27.221:8050;
        server 41.159.27.9:8050;
        server 41.159.117.119:8050;
    }
    server {
        listen 8050;
        location / {
            proxy_pass http://splash;
            auth_basic "Restricted";
            auth_basic_user_file /etc/nginx/conf.d/.htpasswd;
        }
    }
}
'''
# 这里使用的用户名和密码配置放置在/etc/nginx/conf.d目录下，需要使用htpasswd命令创建
# 例如，创建一个用户名为admin的文件，相关命令如下：
# htpasswd -c .htpasswd admin
# 接下来会提示输入密码，输入两次后，就会生成密码文件，其内容如下：
# cat .htpasswd
# admin:5ZBxQr0rCqwbc
# 配置完成后，重启一下Nginx服务
# nginx -s relaod
"""
