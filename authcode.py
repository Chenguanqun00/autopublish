#!/usr/bin/python3
#encoding: utf-8
'''
@File: authcode.py
@Author:limz
@Time: 2019年03月12日22时
'''
import cv2
import numpy as np

def math_img(image,Target,value):
    distance = 0
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    # cv2.imshow('rgb', img_rgb)
    # cv2.imshow('gray', img_gray)
    # cv2.imshow('template', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
        distance = pt[0]
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    return distance
image = "image.jpg"
Target = "target.png"
value = 0.7
#math_img(image, Target, value)