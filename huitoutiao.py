#!/usr/bin/python3
#encoding: utf-8
'''
@File: huitoutiao.py
@Author:limz
@Time: 2019年03月20日21时
'''

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import os
import shutil
from PIL import Image

#登陆
def login(url, username, password):
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_driver = r'C:\Users\ADMIN\AppData\Local\CentBrowser\Application\chromedriver.exe'
    chrome_driver = r'D:\Program Files\CentBrowser\CentBrowser\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)


    input1 = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/input')
    input2 = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[3]/input')
    input1.send_keys(username)
    time.sleep(2)
    input2.send_keys(password)
    time.sleep(2)

    #点击登陆
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div[5]/button').click()
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
    i = 1
    names = []
    for img in imgs:
        driver.find_element_by_xpath('//div[@id="editor"]/div').send_keys(imgs[img])
        driver.find_element_by_xpath('//div[@class="w-e-toolbar"]/div[5]/i').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="w-e-up-img-container"]/div[2]/input').send_keys(img)
        i += 1
        names.append(imgs[img])
        time.sleep(5)
    return names

#给图片加名字
def uploadname():
    m = 1
    for name in names:
        driver.find_element_by_xpath('//div[@id="imedia-article"]/div[' + str(m) + ']/div/span[@class="image-caption-wrap"]/input').send_keys(name)
        time.sleep(1)
        m += 1

if __name__ == '__main__':
    username = "18215565025"                      #用户名
    password = "wanglihong123"                      #密码
    url = "https://mp.cashtoutiao.com/user/login"    #登陆地址
    gifpath = r"E:\ziyuan\gif"                  #GIF资源路径
    gifnewpath = r"E:\自媒体\已发表\GIF\{0}\{1}".format(time.strftime("%Y%m%d", time.localtime()), "惠头条")    #新GIF存放路径
    jpgpath = r"E:\ziyuan\pic"                  #pic资源路径
    jpgnewpath = r"E:\自媒体\已发表\pic\{0}\{1}".format(time.strftime("%Y%m%d", time.localtime()), "惠头条")    #新pic存放路径
    gifcount = 10                               #筛选gif图片数量
    jpgcount = 3                                #筛选jpg图片数量
    giftype = 'gif'
    jpgtype = 'jpg'

    #打开登陆页面获取验证码
    print("登陆中...")
    driver = login(url, username, password)

    #点击创作按钮
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[1]/ul/li[1]/div').click()

    #点击发表
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[1]/ul/li[1]/ul/li[1]').click()

    # #点击上传图片
    # time.sleep(2)
    # driver.find_element_by_xpath('//div[@class="w-e-toolbar"]/div[5]/i').click()

    #从本地资源中随机选择GIF图片
    time.sleep(2)
    print("筛选GIF图片...")
    imgs = get_newfile(gifcount, gifpath, gifnewpath, giftype)

    #上传GIF图片
    print("上传GIF图片...")
    names = uploadpic(imgs)

    #从本地资源中随机选择jpg图片
    time.sleep(2)
    print("筛选jpg图片...")
    imgs = get_newfile(jpgcount, jpgpath, jpgnewpath, jpgtype)

    # 上传JPG图片
    print("上传jpg图片...")
    uploadpic(imgs)

    # 随机从名字中生成一个标题
    print("添加标题...")
    title = "搞笑GIF：" + names[random.randint(0, len(names) - 1)]
    # 加标题
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[1]/div[1]/input').send_keys(title)
    time.sleep(5)

    #滑动到页面底部
    time.sleep(2)
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)

    # #选择封面设置为自动
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[3]/ul/li[2]/div[1]/label[3]/input').click()

    # #选择分类
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[4]/div[2]/div/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[4]/div[2]/div[2]/ul/li[3]/ul/li[1]').click()

    #标签
    label = ["搞笑", "逗逼", "GIF"]
    for i in label:
        driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[5]/label/div/input').send_keys(i)
        driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[4]/div[2]/div/input').click()

    # #发表
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div[2]/div/ul/li[6]/div/button[1]').click()

    #确认发布
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[2]').click()
