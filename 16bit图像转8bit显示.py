# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/09/09
# Description : 16位图像转8位图像程序 
# 读入图像 每个像素与0xFF“逻辑与”操作 输出



import numpy as np
import struct


def raw_file_output16(fname, raw_data):
    with open(fname, 'wb') as f:
        raw_data[raw_data < 0] = 0  # 除去负数
        for i in raw_data.flat:          
            foo = struct.pack('H', int(i))
            f.write(foo)

def raw_file_output8(fname, raw_data):
    with open(fname, 'wb') as f:
        raw_data[raw_data < 0] = 0  # 除去负数
        for i in raw_data.flat:          
            foo = struct.pack('B', int(i))
            f.write(foo)
            
fname = '50.raw'
raw_data = np.fromfile(fname, dtype=np.uint16)

raw_data = raw_data & 0xFF
raw_data.astype(np.int8)

fout = '50-8.raw'
raw_file_output8(fout, raw_data)