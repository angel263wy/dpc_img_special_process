# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/06/21
# Description :  杂光实时处理软件
# 文件夹及文件数量合理性判断
'''
输入参数 main中前几行  图像宽高 拼图阈值 杂光目录
    raw_width = 1024
    raw_height = 1030
    dn_threhold_ratio = 0.85  # 拼图用的二值化 比例 即最大值的百分比作为阈值 小于该值的为0
    stray_light_path = 'f:\\sl\\'   # 杂光目录 里面应该全是5,5  3,34这类文件夹 没有其他文件夹
输出
    stray_light_path目录下新建了一个img_mean文件夹 里面有31个文件夹 对应31个状态 即14个通道线性区和饱和区 3个本底通道积分时间
    stray_light_path目录下新建了一个combine_img文件夹 用于存放拼图
'''

import numpy as np
import os
import glob
import struct
import time
from enum import Enum,unique
from multiprocessing import Process, Queue

# 每次成像的枚举类型
@unique
class enum_Img_Sequence(Enum):
    lin_490P1 = 0
    sat_490P1 = 1
    lin_490P2 = 2
    sat_490P2 = 3
    lin_490P3 = 4
    sat_490P3 = 5
    lin_565 = 6
    sat_565 = 7
    lin_670P1 = 8
    sat_670P1 = 9
    lin_670P2 = 10
    sat_670P2 = 11
    lin_670P3 = 12
    sat_670P3 = 13
    lin_763 = 14
    sat_763 = 15
    lin_765 = 16
    sat_765 = 17
    lin_865P1 = 18
    sat_865P1 = 19
    lin_865P2 = 20
    sat_865P2 = 21
    lin_865P3 = 22
    sat_865P3 = 23
    lin_443 = 24
    sat_443 = 25
    lin_910 = 26
    sat_910 = 27
    lin_dk20 = 28
    lin_dk80 = 29
    sat_dk1000 = 30


def raw_file_output(fname, raw_data):
    with open(fname, 'wb') as f:
        raw_data[raw_data < 0] = 0  # 除去负数
        raw_data[raw_data > 65535] = 65535  # 除去负数
        for i in raw_data.flat:            
            foo = struct.pack('H', int(i))
            f.write(foo)



'''
单个光阑处理函数
读入光阑文件文件夹 检查文件夹内目录数量 检查每个通道文件数量
每个通道文件逐像元求均值 
'''
def aperture_process(sl_path, aperture_queue, raw_width, raw_height):
    
    os.chdir(sl_path)
    # 队列非空 进行处理
    while aperture_queue.qsize() :
        # 第一部分 导入文件夹 判断文件夹数量
        raw_path = aperture_queue.get()  # 杂光光阑编号 例如5-5 或者 1-4                 
        img_folder = glob.glob(raw_path + '\\*')  # 获取一个光阑下的所有文件夹 存储30个文件夹
        if len(img_folder) == 30 :
            print('光阑编号' + raw_path + '  文件夹数量' + str(len(img_folder))+ '  数量正确')
        else:
            print('光阑编号' + raw_path + '  文件夹数量' + str(len(img_folder)) + '  不满足要求')
            return
        
        
        # 第二部分 处理当前光阑文件夹下图像
        # 1.判断文件数量合理性
        err = False
        for img_dir in img_folder:
            fnames = glob.glob(img_dir + '\\RAW_ImageData\\*.raw')
            if (len(fnames) != 29) and (len(fnames) != 59):
                print('文件夹 ' + img_dir + ' 文件数量' + str(len(fnames)) + ' 不正确')
                err = True
        if err:
            return   


if __name__ == "__main__":
    raw_width = 1024
    raw_height = 1030    
    stray_light_path = 'f:\\wangyi\\'
    os.chdir(stray_light_path)
    raw_dir = glob.glob('*')
    
    aperture_queue = Queue()  # 光阑队列 进入队列的为每个光阑的文件夹名称
    for dirs in raw_dir :
        if (dirs == 'combine_img') or (dirs == 'img_mean'):
            pass
        else:
            aperture_queue.put(dirs)
    
    
    # aperture_process(stray_light_path, aperture_queue, raw_width, raw_height)           
    
    p1 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))
    p2 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))
    p3 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))
    p4 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))
    p5 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))
    p6 = Process(target=aperture_process, args=(stray_light_path, aperture_queue, raw_width, raw_height))

    print(time.strftime('%Y%m%d-%H%M%S ', time.localtime(time.time())))
    # p_l = [p1, p2, p3]
    p_l = [p1, p2, p3, p4, p5, p6]
    for p in p_l:
        p.start()
    for p in p_l:
        p.join()
        
    # print(time.strftime('%Y%m%d-%H%M%S ', time.localtime(time.time())))
    print('aperture process end')
    
    band_queue = Queue()  # 31个文件夹队列
    for band in enum_Img_Sequence:
        band_queue.put(band.name)
    

    
    print(time.strftime('%Y%m%d-%H%M%S ', time.localtime(time.time())))
    print('end')
    






