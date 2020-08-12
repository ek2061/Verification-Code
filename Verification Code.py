# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 00:03:03 2020

@author: Yuchi
"""

import cv2
import numpy as np
import random, string
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import matplotlib.pyplot as plt

img_width = 240
img_height = 60

def getRandomChar():  #生成隨機英數
    return random.choice(string.ascii_letters + string.digits)

def getRandomColor():  #生成隨機 RGB
    return random.randint(50, 300), random.randint(50, 150), random.randint(50, 150)
    
def getRandomFont():  #生成隨機字體大小
    return random.randint(int(img_width*0.2), int(img_width*0.23))

def getRandomAngle():
    angle = random.randint(15, 25)
    r = random.randint(0, 2)
    if r == 0:
        return angle
    else:
        return -angle

def create_code():
    font_path = r'C:\Windows\Fonts\Arial.ttf'
    res = np.zeros([img_height, img_width, 3] , dtype = 'int16')
    a = []
    b = ['l', 'I']  #我不要的英數字
    
    for i in range(4):
        img = Image.new('RGB', (img_height, img_height), (255, 255, 255))  #創建圖片
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, getRandomFont())  #字體
        code = getRandomChar()  #英數字
        while code in a or code in b:  #檢查重複
            code = getRandomChar()  #英數字
        a.append(code)
        draw.text((img_height/6, 0), code, getRandomColor(), font)
        
        np_img = np.array(img)
        
        angle = getRandomAngle()  #旋轉角度
        center = (img_height/2, img_height/2)  #中心點
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(np_img, M, (img_height, img_height), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE, borderValue = (255, 255, 255))
        
        pts1 = np.float32([[0, 0],[0, 60],[60, 60],[60, 0]])
        pts2 = np.float32([[10, 0],[-10, 30],[50, 60],[70, 0]])
        warp_mat = cv2.getPerspectiveTransform(pts1, pts2)  #透視變換
        dst = cv2.warpPerspective(rotated, warp_mat, (img_height, img_height), borderValue = (255, 255, 255))
        
        res[:, img_height*i:img_height*(i+1), :] = dst  #把每張處理過的結果拼起來
    
    img = Image.fromarray(np.uint8(res))
    draw = ImageDraw.Draw(img)
    
    point_num = random.randint(img_height*10, img_height*20)  #干擾點數量
    for _ in range(point_num):
        pos_x = random.randint(0, img_width)
        pos_y = random.randint(0, img_height)
        draw.point([pos_x, pos_y], fill = getRandomColor())  
    
    line_num = random.randint(2, 5)  #干擾線數量
    for _ in range(line_num):
        pos_start = (random.randint(0, img_width), random.randint(0, img_height))  #線的起始座標
        pos_end = (random.randint(0, img_width), random.randint(0, img_height))  #線的結束座標
        draw.line([pos_start, pos_end], fill = getRandomColor())
    
    ans = ''
    for i in a:
        ans += i
    img.save(ans + '.jpg', 'jpeg')
    return img, ans

if __name__ =='__main__':
    i, a = create_code()
    plt.figure('Verification Code')
    plt.imshow(i)
    print('ans is ', a)