# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2021/04/07
# Description : CM每轨首帧问题排查程序 
#  读入当前文件夹所有图像 提取左上角2X2像元DN值并输出


import numpy as np
import time
import os
import glob
from pathlib import Path



now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
fname = f'CM首帧图像问题日志.txt'

# 日志记录
def log(filename, context):
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(context)
        f.write('\n')
        print(context)

filelist = glob.glob('*.raw')
for filename in filelist:
    raw_data = np.fromfile(filename, dtype=np.uint16).reshape(380, 512)
    a = raw_data[0, 0]
    b = raw_data[0, 1]
    c = raw_data[1, 0]
    d = raw_data[1, 1]
    log(fname, f'文件{filename} 图像左上角2X2像素值分别为 {a} {b} {c} {d}')
    
print('end')       




