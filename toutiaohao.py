#!/usr/bin/python3
#encoding: utf-8
'''
@File: toutiaohao.py
@Author:limz
@Time: 2019年03月11日23时
'''


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from authcode import math_img

def getpic(path, url):
    res = requests.get(url)
    with open(path, 'wb') as file:
        file.write(res.content)
        file.flush()

def get_track(distance):
    track = []
    current = 0
    mid = distance*3/4
    t = random.randint(2, 3)/10
    v = 0
    while current < distance:
          if current < mid:
             a = 2
          else:
             a = -3
          v0 = v
          v = v0+a*t
          move = v0*t+1/2*a*t*t
          current += move
          track.append(round(move))
    return track

def start(image, target, url, username, password):
    global imageurl, targeturl
    driver = webdriver.Chrome(r'D:\Program Files\CentBrowser\CentBrowser\Application\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    #跳转到账号密码登录
    getaccount=driver.find_element_by_id('login-type-account')
    getaccount.click()

    input1 = driver.find_element_by_id('user-name')
    input2 = driver.find_element_by_id('password')
    input1.send_keys(username)
    input2.send_keys(password)
    time.sleep(0.2)
    #获取打开滑块验证码页面的元素
    getcheck=driver.find_element_by_id('bytedance-login-submit')
    #点击进入滑块验证码页面
    getcheck.click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #获取验证码的下载地址
    imageurl = soup.find(attrs={"id": "validate-big"}).get("src")
    targeturl = soup.find(attrs={"class": "validate-block"}).get("src")
    getpic(image, imageurl)
    getpic(target, targeturl)
    return driver

def track(driver, distance):
    slideblock = driver.find_element_by_class_name("drag-button")
    #ActionChains(driver).click_and_hold(slideblock).perform()
    track_list=get_track(distance+3)
    time.sleep(2)
    ActionChains(driver).click_and_hold(slideblock).perform()
    time.sleep(0.2)
    # 根据轨迹拖拽圆球
    for track in track_list:
        ActionChains(driver).move_by_offset(xoffset=track,yoffset=0).perform()
    # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
    imitate=ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
    time.sleep(0.015)
    imitate.perform()
    time.sleep(random.randint(6,10)/10)
    imitate.perform()
    time.sleep(0.04)
    imitate.perform()
    time.sleep(0.012)
    imitate.perform()
    time.sleep(0.019)
    imitate.perform()
    time.sleep(0.033)
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    # 放开圆球
    ActionChains(driver).pause(random.randint(6,14)/10).release(slideblock).perform()
    time.sleep(2)
    #务必记得加入quit()或close()结束进程，不断测试电脑只会卡卡西
    #driver.close()

image = "image.jpg"
target = "target.png"
value = 0.7
username = "18215565025"
password = "Wanglihong123"
url = "https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG"
driver = start(image, target, url, username, password)
distance = math_img(image, target, value)
while distance == 0:
    driver.close()
    driver = start(image, target, url, username, password)
    distance = math_img(image, target, value)
print(distance)
track(driver, distance)

# cookies1 = driver.get_cookies()
# cookies = {}
# for i in cookies1:
#     cookies[i["name"]] = i["value"]
# url = "https://mp.toutiao.com/tools/upload_picture/?type=ueditor&pgc_watermark=1&action=uploadimage&encode=utf-8"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Referer": "https://mp.toutiao.com/profile_v3/graphic/publish"}
# type = "image/jpeg"
# with open("image.jpg", "rb") as file:
#     upfile = file.read()
# res = requests.post(url, data={"type": "image/jpeg", "upfile": upfile}, headers=headers, cookies=cookies)
# print(res.status_code)
# print(res.content)
#点击发布
time.sleep(4)
driver.find_elements_by_class_name('tui2-menu-item')[1].click()
time.sleep(1)
#上传图片
driver.find_element_by_class_name('ql-image').click()
time.sleep(1)
#选择图片
#print(driver.find_elements_by_tag_name('input'))
driver.find_element_by_xpath("//span[@class='syl-img-upload']/input").send_keys(r'C:\Users\Administrator\Desktop\code\autopublish\image.jpg')
time.sleep(1)
driver.find_element_by_xpath("//span[@class='syl-img-upload']/input").send_keys(r'C:\Users\Administrator\Desktop\code\autopublish\toobig.gif')
time.sleep(5)
driver.find_element_by_xpath("//button[@data-e2e='imageUploadConfirm-btn']").click()
