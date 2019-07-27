from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 模拟浏览器运行的库——selenium和splash
# 如果遇到版本错误异常则需要将浏览器驱动更新至对应的浏览器版本
# 更新方法：https://www.cnblogs.com/sxming/p/7662945.html
# 驱动下载地址：http://npm.taobao.org/mirrors/chromedriver/


"""2、Selenium的使用"""
# Selenium是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，如点击、下拉等操作，同时还可以获取浏览器当前呈现的页面的源代码，做到可见即可爬，非常利于抓取动态渲染的页面
"""基本使用方法
# 模拟浏览器使用百度搜索python相关内容
browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()
"""


"""3、声明浏览器对象
# selenium支持非常多浏览器，如Chrome、Firefox、Edge等，还有Android手机端的浏览器
browser = webdriver.Chrome()  # 浏览器对象初始化，赋值为browser对象
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.Safari()
browser = webdriver.Opera()
browser = webdriver.PhantomJS()
"""


"""4、访问页面
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')  # 使用get()方法请求页面
print(browser.page_source)
browser.close()
"""


"""5、查找节点"""
# selenium可以驱动浏览器完成各种操作，比如填充表单、模拟点击
"""单个节点
# 从淘宝网中提取搜索框这个节点
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')  # 查找id=q节点
# input_first = browser.find_element(By.ID, 'q')  # 通用方法find_element()，传入两个参数：查找方式By和值
input_second = browser.find_element_by_css_selector('#q')  # CSS选择器查找属性值为'q'的节点
input_third = browser.find_element_by_xpath('//*[@id="q"]')  # xpath解析所有id属性值为q的节点
print(input_first, input_second, input_third)
browser.close()
"""


"""多个节点
# 查找淘宝左侧导航条的所有条目
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')  # 获取class属性值为service-bd的所有li节点
# lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')  # 同样可以使用find_elements()通用方法
print(lis)  # 返回一个列表
browser.close()
"""


"""6、节点交互
# 浏览器模拟操作，常见方法有：
# send_keys()——输入文字
# clear()——清空文字
# click()——点击按钮
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')  # 获取搜索框
input.send_keys('iPhone')  # 输入文字
time.sleep(2)
input.clear()  # 清空文字
input.send_keys('iPad')  # 输入文字
button = browser.find_element_by_class_name('btn-search')  # 获取搜索按钮
button.click()  # 模拟点击按钮
browser.close()
"""


"""7、动作链
# 鼠标拖拽、键盘按键属于动作链操作
browser = webdriver.Chrome()
url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')  # 选中拖拽实例
source = browser.find_element_by_css_selector('#draggable')  # 源节点
target = browser.find_element_by_css_selector('#droppable')  # 目标节点
actions = ActionChains(browser)  # 声明ActionChains对象
actions.drag_and_drop(source, target)  # 调用拖拽方法
actions.perform()  # 执行操作
browser.close()
"""


"""8、执行JavaScript
# 使用execute_script()方法模拟运行JavaScript
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 将进度条下拉到最底部
browser.execute_script('alert("To Bottom")')  # 弹出alert提示框
browser.close()
"""


"""9、获取节点信息"""
"""获取属性
# 使用get_attribute()方法来获取节点的属性，但是前提是先选中这个节点
browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
logo = browser.find_element_by_id('zh-top-link-logo')  # 获取知乎的logo节点
print(logo)
print(logo.get_attribute('class'))  # 打印出class的值
browser.close()
"""


"""获取文本值
# 每个WebElement节点都有text属性，直接调用这个属性就可以得到节点内部的文本信息
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.text)
browser.close()
"""


"""获取id、位置、标签名和大小
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.id)  # 节点id
print(input.location)  # 节点在页面中的相对位置
print(input.tag_name)  # 标签名称
print(input.size)  # 节点大小，即宽高
browser.close()
"""


"""10、切换Frame
# 网页中有一种节点叫作iframe，也就是子Frame，相当于页面的子页面，它的结构和外部网页的结构完全一致。
# selenium打开页面后，默认是在父级Frame里面操作，如果此时页面中存在子Frame，是不能获取到子Frame中的节点的
# selenium使用switch_to.frame()方法切换Frame
browser = webdriver.Chrome()
url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')  # 进入子Frame
try:
    logo = browser.find_element_by_class_name('logo')  # 获取logo，但是子Frame中自然是没有的，会抛出异常
except NoSuchElementException:
    print('NO LOGO')
browser.switch_to.parent_frame()  # 切换回父Frame
result = browser.find_element_by_class_name('logo')
print(result)
print(result.text)
browser.close()
"""


"""11、延时等待"""
# 获取页面时，需要延时等待一定时间，确保节点已经加载出来（某些页面有额外的Ajax请求）
# 等待的方式分为两种：隐式等待和显示等待
"""隐式等待
# 如果selenium没有在DOM中找到节点，将继续等待，超出设定时间后，则抛出找不到节点的异常
browser = webdriver.Chrome()
browser.implicitly_wait(10)  # 设置等待时间为10秒
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input)
browser.close()
"""


"""显示等待
# 指定要查找的节点，然后指定一个最长等待时间，如果在规定时间内加载出来了这个节点，就返回查找的节点；如果到了规定时间依然没有加载出该节点，则抛出超时异常
browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser, 10)  # 声明WebDriverWait对象，指定最长等待时间为10秒，然后调用until()方法，传入要等待条件
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))  # presence_of_element_located条件表示节点出现，参数为节点的定位元组，即ID为q的节点搜索框
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))  # element_to_be_clickable条件表示节点可点击
print(input, button)
browser.close()
"""


"""12、前进和后退
# selenium使用back()方法后退，使用forward()方法前进
browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.zhihu.com/')
browser.back()
time.sleep(2)
browser.forward()
browser.close()
"""


"""13、Cookies
# 获取、添加、删除Cookies
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())  # 调用get_cookies()方法获取所有的cookies
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})  # 调用add_cookie()方法添加一个Cookie，需要传入一个字典
print(browser.get_cookies())
browser.delete_all_cookies()  # 调用delete_all_cookies()方法删除所有的Cookies
print(browser.get_cookies())
browser.close()
"""


"""14、选项卡管理
# 在访问网页时，会开启一个个选项卡，selenium可以对选项卡进行操作
browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')  # 传入window.open()语句开启一个新选项卡
print(browser.window_handles)
browser.switch_to.window(browser.window_handles[1])  # 切换到第二个选项卡
browser.get('https://www.taobao.com')
time.sleep(2)
browser.switch_to.window(browser.window_handles[0])  # 切换到第一个选项卡
browser.get('https://zhihu.com')
browser.close()
"""


"""15、异常处理
browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
"""
