#!/usr/bin/python3
#encoding: utf-8
'''
@Author: limz 
@project: autopublish
@file: qiehao.py
@time: 2019/3/19 10:57
@desc:
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
from PIL import Image

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
    options = webdriver.ChromeOptions()
    #chrome_driver = r'C:\Users\ADMIN\AppData\Local\Google\Chrome\Application\chromedriver.exe'
    chrome_driver = r'D:\Program Files\CentBrowser\CentBrowser\Application\chromedriver.exe'
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_css_selector("[class='appClose close']").click()
    except Exception as e:
        pass
    driver.find_element_by_class_name("login-type-qq").click()

    time.sleep(6)
    frame = driver.find_element_by_xpath("//div[@class='ptlogin-container']/iframe")
    driver.switch_to.frame(frame)
    time.sleep(0.5)
    iframe = driver.find_element_by_id("ptlogin_iframe")
    driver.switch_to.frame(iframe)
    #单击账号密码登陆
    driver.find_element_by_xpath("//*[@id='switcher_plogin']").click()

    input1 = driver.find_element_by_id('u')
    input2 = driver.find_element_by_id('p')
    input1.send_keys(username)
    input2.send_keys(password)
    time.sleep(0.2)

    #点击登陆
    driver.find_element_by_id('login_button').click()
    time.sleep(5)

    return driver

#遍历目录下所以文件
def gci(path, allfile):
    parents = os.listdir(path)
    for parent in parents:
        if parent == "forgifs" or parent == "hilariousgifs":
            pass
        else:
            child = os.path.join(path, parent)
            #print(child)
            if os.path.isdir(child):
                gci(child, allfile)
            else:
                allfile.append(child)
                #print(child)
    #print(len(allfile))
    return allfile

#获取旧文件路径
def get_oldgif(allfile):
    oldfile = allfile.pop(random.randint(0, len(allfile) - 1))
    if os.path.getsize(oldfile) >= 5242880:
        oldfile = get_oldgif(allfile)
    return oldfile

def get_oldjpg(allfile):
    oldfile = allfile.pop(random.randint(0, len(allfile) - 1))
    img = Image.open(oldfile)
    long = img.size[0]
    width = img.size[1]
    if long < 360 or width <270:
        oldfile = get_oldjpg(allfile)
    return oldfile

#获取新文件路径
def get_newfile(count, path, newpath,type):
    files = []
    allfile = gci(path, files)
    filelist = []
    imgs = {}
    for i in range(count):
        if type == 'gif':
            oldfile = get_oldgif(allfile)
        else:
            oldfile = get_oldjpg(allfile)
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
        if filename.endswith('.gif') or filename.endswith('.jpg'):
            name = filename.split('.')[0]
            imgs[file] = name
    return imgs

#上传图片
def uploadpic(imgs):
    i = 2
    names = []
    for img in imgs:
        driver.find_element_by_class_name("webuploader-element-invisible").send_keys(img)
        wait = WebDriverWait(driver, 20)
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//ul[@id="queueList"]/li[' + str(i) + ']/span[@class="success"]')))
            print('success:%s' % img)
            names.append(imgs[img])
        except Exception as e:
            print("上传失败，路径：%s,报错信息：%s" % (img, str(e)))
        i += 1
    time.sleep(5)
    driver.find_element_by_class_name("layui-layer-btn0").click()
    return names

#给图片加名字
def uploadname():
    m = 0
    iframe = driver.find_element_by_id("ueditor_0")
    driver.switch_to.frame(iframe)
    for name in names:
        js = 'document.getElementsByClassName("imagenote")[' + str(m) + '].innerHTML="' + name + '"'
        driver.execute_script(js)
        time.sleep(1)
        m += 1

if __name__ == '__main__':
    username = "694314541"                      #用户名
    password = "li@648236"                      #密码
    url = "https://om.qq.com/userAuth/index"    #登陆地址
    gifpath = r"E:\ziyuan\gif"                  #GIF资源路径
    gifnewpath = r"E:\自媒体\已发表\GIF\{0}\{1}".format(time.strftime("%Y%m%d", time.localtime()), "企鹅号")    #新GIF存放路径
    jpgpath = r"E:\ziyuan\pic"                  #pic资源路径
    jpgnewpath = r"E:\自媒体\已发表\pic\{0}\{1}".format(time.strftime("%Y%m%d", time.localtime()), "企鹅号")    #新pic存放路径
    gifcount = 10                               #筛选gif图片数量
    jpgcount = 3                                #筛选jpg图片数量
    giftype = 'gif'
    jpgtype = 'jpg'

    #打开登陆页面获取验证码
    print("登陆中...")
    driver = login(url, username, password)

    # #点击发布按钮
    time.sleep(5)
    driver.find_elements_by_class_name('menu-sub-text')[0].click()

    # #点击上传图片
    time.sleep(4)
    driver.find_element_by_css_selector("[class='edui-box edui-icon edui-om']").click()

    #从本地资源中随机选择GIF图片
    time.sleep(2)
    print("筛选GIF图片...")
    imgs = get_newfile(gifcount, gifpath, gifnewpath, giftype)

    #上传GIF图片
    print("上传GIF图片...")
    names = uploadpic(imgs)

    #随机从名字中生成一个标题
    print("添加标题...")
    title = "搞笑GIF：" + names[random.randint(0, len(names)-1)]
    #加标题
    driver.find_element_by_xpath('//*[@id="om-art-normal-title"]/div/label/input').send_keys(title)
    time.sleep(5)

    #给图片加上名字
    print("加名字...")
    uploadname()

    #从本地资源中随机选择jpg图片
    time.sleep(2)
    print("筛选jpg图片...")
    imgs = get_newfile(jpgcount, jpgpath, jpgnewpath, jpgtype)

    #切换回默认frame
    driver.switch_to.default_content()

    #点击上传图片
    time.sleep(2)
    driver.find_element_by_css_selector("[class='edui-box edui-icon edui-om']").click()

    # 上传JPG图片
    print("上传jpg图片...")
    uploadpic(imgs)

    #滑动到页面底部
    time.sleep(2)
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)

    # #选择封面设置为自动
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="checkbox-inline"]/label[2]/i').click()

    # #选择分类
    driver.find_element_by_xpath('//div[@class="form-inline"]/div[2]/div').click()

    # #发表
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="inline-block"]/button').click()

    #确认发布
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="pop-action"]/button[2]').click()
    time.sleep(2)
    driver.find_element_by_class_name('layui-layer-btn0').click()