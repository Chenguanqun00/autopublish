#!/usr/bin/python3
#encoding: utf-8
'''
@File: dayuhao.py
@Author:limz
@Time: 2019年03月16日17时
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
import os
import shutil

#下载
def getpic(path, url):
    res = requests.get(url)
    with open(path, 'wb') as file:
        file.write(res.content)
        file.flush()

#生成运动轨迹列表
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

#登陆
def login(url, username, password):
    driver = webdriver.Chrome(r'D:\Program Files\CentBrowser\CentBrowser\Application\chromedriver.exe')
    #driver = webdriver.Chrome(r'C:\Users\ADMIN\AppData\Local\CentBrowser\Application\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    frame = driver.find_element_by_xpath("//div[@class='loginPage-login_body']/iframe")
    driver.switch_to.frame(frame)
    input1 = driver.find_element_by_id('login_name')
    input2 = driver.find_element_by_id('password')
    input1.send_keys(username)
    input2.send_keys(password)
    time.sleep(0.2)

    #滑动滑块
    track(driver)
    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, '验证通过')))
        print('success')
    except Exception as e:
        print("失败")

    #点击登陆
    driver.find_element_by_id('submit_btn').click()
    time.sleep(5)

    return driver

#执行滑动实现登陆
def track(driver):

    # 获取需要滑动的距离
    distance = 188

    track_list = get_track(distance)
    time.sleep(2)
    slideblock = driver.find_element_by_xpath('//div[@id="nocaptcha"]/div/div/span')
    ActionChains(driver).click_and_hold(slideblock).perform()
    time.sleep(0.2)

    ActionChains(driver).move_by_offset(xoffset=distance, yoffset=0).perform()

    # 根据轨迹拖拽圆球
    # for track in track_list:
    #     ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

    time.sleep(2)
    #务必记得加入quit()或close()结束进程，不断测试电脑只会卡卡西
    #driver.close()

#遍历目录下所以文件
def gci(path):
    """this is a statement"""
    parents = os.listdir(path)
    for parent in parents:
        if parent == "forgifs" or parent == "hilariousgifs":
            pass
        else:
            child = os.path.join(path,parent)
            #print(child)
            if os.path.isdir(child):
                gci(child)
            else:
                filepath.append(child)
                #print(child)

#获取新文件
def get_newfile(count):
    gci(path)
    filelist = []
    imgs = {}
    for i in range(count):
        oldfile = filepath.pop(random.randint(0, len(filepath) - 1))
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        newfile = os.path.join(newpath, os.path.basename(oldfile))
        filelist.append(newfile)
        shutil.copyfile(oldfile, newfile)
        print("已复制新文件：%s" % newfile)
        os.remove(oldfile)
        print("已删除旧文件：%s" % oldfile)
    for file in filelist:
        filename = os.path.basename(file)
        if filename.endswith('.gif'):
            name = filename.split('.')[0]
            imgs[file] = name
    return imgs

#上传图片
def uploadpic(imgs):
    i = 1
    names = []
    for img in imgs:
        driver.find_element_by_xpath("//span[@class='syl-img-upload']/input").send_keys(img)
        wait = WebDriverWait(driver, 20)
        try:
            flag = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//ul[@class="image-list"]/li[' + str(i) + ']/div[@class="success"]')))
            print('success:%s' % img)
            names.append(imgs[img])
        except Exception as e:
            print("上传失败，路径：%s,报错信息：%s" % (img, str(e)))
        i += 1
    time.sleep(5)
    driver.find_element_by_xpath("//button[@data-e2e='imageUploadConfirm-btn']").click()
    return names

#给图片加名字
def uploadname():
    m = 1
    for name in names:
        if m > 1:
            name = "1" + name
        for n in name:
            driver.find_element_by_xpath('//div[@class="ql-editor"]/tt-image[' + str(
                m) + ']/div/div[@class="pgc-img-caption-wrapper"]/input').send_keys(n)
        time.sleep(1)
        m += 1

if __name__ == '__main__':
    username = "694314541@qq.com"       #用户名
    password = "wanglihong123"     #密码
    url = "https://mp.dayu.com/"    #登陆地址
    path = r"E:\ziyuan\gif"        #资源路径
    newpath = r"E:\自媒体\已发表\GIF\{0}\{1}".format(time.strftime("%Y%m%d", time.localtime()), "大鱼号")    #新图片存放路径
    filepath = []                  #保存新图片路径
    count = 10                     #筛选图片数量

    #打开登陆页面获取验证码
    print("登陆中...")
    driver = login(url, username, password)

    # #点击发布按钮
    # time.sleep(9)
    # driver.find_elements_by_class_name('tui2-menu-item')[1].click()
    #
    # #点击上传
    # time.sleep(4)
    # driver.find_element_by_class_name('ql-image').click()
    #
    # #从本地资源中随机选择图片
    # time.sleep(2)
    # print("筛选图片...")
    # imgs = get_newfile(count)
    #
    # #上传图片
    # print("上传图片...")
    # names = uploadpic(imgs)
    #
    # #随机从名字中生成一个标题
    # print("添加标题...")
    # title = "搞笑GIF：" + names[random.randint(0, len(names)-1)]
    # #加标题
    # driver.find_element_by_xpath('//div[@class="syl-editor-input"]/span/input').send_keys(title)
    # time.sleep(5)
    #
    # #给图片加上名字
    # print("加名字...")
    # uploadname()
    #
    # #滑动到页面底部
    # js = "var q=document.documentElement.scrollTop=100000"
    # driver.execute_script(js)
    #
    # #选择封面设置为自动
    # driver.find_element_by_xpath('//div[@class="article-cover"]/div[@class="tui2-radio-group"]/label[3]/div/input').click()
    #
    # #发表
    # time.sleep(2)
    # #driver.find_element_by_id("publish").click()