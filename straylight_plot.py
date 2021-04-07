# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2021/02/02
# Description : 杂光绘图软件 将拼好的图片按行按列画曲线
'''
挑行算法
输入起始行 根据起始行依次加100行
'''


import numpy as np
import os
import glob
import struct
import time
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False 

img_path = 'f:\\sl\\combine_img\\*.raw'

filelist = glob.glob(img_path)

start_row = 25
row_cnt = np.arange(start_row, 1030, 95)

start_col = 25
col_cnt = np.arange(start_col, 1030, 95)

if len(filelist) == 0:
    print('未找到文件 处理结束')
else:
    # 对每个文件画图
    for fname in filelist :
        # 读入文件 形成图像
        raw_data = np.fromfile(fname, dtype=np.uint16).reshape(1030, 1024)
        y_row = raw_data[row_cnt]  #挑行画图
        y_col = raw_data[col_cnt]  #挑列画图
                
        plt.figure()
        plt.subplot(211)
        plt.title(f'上图按行 下图按列 挑数画图--{fname}')

        for cnt in range(y_row.shape[0]):  # 按行画图 shape[0]表示行
            plt.plot(y_row[cnt])
        
        plt.subplot(212)
        plt.xlabel('坐标')
        plt.ylabel('灰度值')
        for cnt in range(y_col.shape[0]):  # 按行画图 shape[0]表示行
            plt.plot(y_col[cnt])
        plt.show()
        

print('end')


