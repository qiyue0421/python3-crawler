# 许多网站采用验证码来反爬虫，验证码有普通图形验证码、极验滑动验证码、点触验证码、微博宫格验证码等等。
import tesserocr
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from io import BytesIO
import time



"""1、图形验证码的识别
# 图形验证码比较常见，一般由4位字母或数字组成。

'''# 从下列地址取得中国知网的图形验证码
# http://my.cnki.net/elibregister/commonRegister.aspx
image = Image.open('CheckCode.jpg')  # 利用本地的CheckCode.jpg文件新建了一个Image对象
text = tesserocr.image_to_text(image)  # 调用tesserocr的image_to_text()方法进行文本的识别
print(text)
'''

# 上述方法识别的实际结果会有偏差，这是因为验证码内的多余线条干扰了图片的识别，对于这种情况，我们需要优先对图片进行相关处理——灰度转换、二值化操作等
image = Image.open('CheckCode.jpg')
image = image.convert('L')  # convert()方法传入参数L可以将图片转化为恢复图像。如果传入1即可进行二值化处理。
threshold = 140  # 指定二值化的阈值
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
result = tesserocr.image_to_text(image)
print(result)
"""


"""2、极验滑动验证码的识别
# 极验滑动验证码需要拖动拼合滑块才能完成验证，相对图形验证码来说识别难度上升了几个等级。
# 极验验证码官网为：http://www.geetest.com/

# 验证识别需要完成以下三步：
# 1）模拟点击验证按钮
# 使用Selenium模拟点击按钮

# 2）识别滑动缺口的位置
# 利用和原图对比检测的方式来识别缺口的位置，因为在没有滑动滑块之前，缺口并没有呈现；
# 对此，我们可以同时获取两张图片，设定一个对比阈值，然后遍历两张图片，找出相同位置像素RGB值差距超过此阈值的像素点，那么此像素点的位置就是缺口的位置

# 3）模拟拖动滑块
# 由于极验验证码增加了机器轨迹识别，匀速运动、随机速度移动等方法都不能通过验证，只有完全模拟人的移动轨迹（一般都是先加速后减速）才能通过验证。

# 选定的测试链接为：https://auth.geetest.com/login/（极验的管理后台登录页面）
# 注：2019/9/22测试该网站已经设置为点触验证，不再使用滑块验证，所以下列代码无法正常运行，不过思路值得一看
# 代码如下
EMAIL = 'test@test.com'
PASSWORD = '123456'


class CrackGeetest():
    # 初始化
    def __init__(self):
        self.url = 'https://auth.geetest.com/login/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    # 打开网页
    def open(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type=email]')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type=password]')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    # 模拟点击初始的验证按钮，利用显式等待的方法实现
    def get_geetest_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))  # 获取初始验证按钮
        return button  # 返回的是一个WebElement对象

    # 获取不带缺口的图片
    # 获取网页截图
    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    # 获取验证码位置
    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    # 获取验证码图片
    def get_geetest_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))  # crop()方法裁剪图片
        captcha.save(name)
        return captcha

    # 获取带缺口的图片，要使得图片出现缺口，只需要点击下方的滑块即可
    # 获取滑块
    def get_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    # 判断两张图片的像素是否相同，如果差距在一定范围内则视为相同，超过范围的像素点代表缺口位置
    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        # 判断像素点的RGB数据是否在规定范围内
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    # 获取缺口位置
    def get_gap(self, image1, image2):
        left = 60  # 直接设置遍历的其实坐标为60，避免识别到滑块（因为滑块的位置都会出现在图片的左边位置）
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    # 根据偏移量获取移动轨迹
    # 直接模拟物理学的加速度公式即可完成验证
    # x = v0 * t + 0.5 * a * t * t
    # v = v0 + a * t
    def get_track(self, distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                a = 2  # 设置加速度为正2
            else:
                a = -3  # 设置加速度为负3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            track.append(round(move))
        return track

    # 根据偏移量拖动轨迹
    def move_to_gap(self, slider, tracks):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).release().perform()

    # 主程序
    def crack(self):
        self.open()
        button = self.get_geetest_button()
        button.click()

        image1 = self.get_geetest_image()
        slider = self.get_slider()
        slider.click()
        image2 = self.get_geetest_image()

        distance = self.get_gap(image1, image2)  # 缺口位置
        distance -= 6  # 减去缺口位移
        track = self.get_track(distance)
        self.move_to_gap(slider, track)


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()
"""


"""点触验证码的识别
# 直接点击图中符合要求的图，所有答案均正确，验证才会成功；如果有一个答案错误，验证就会失败。这种验证码就称为点触验证码
"""


"""微博宫格验证码的识别
# 每个宫格之间会有一条指示连线，指示了应该的滑动轨迹，要按照滑动轨迹依次从起始宫格滑动到终止宫格，才可以完成验证。
"""
