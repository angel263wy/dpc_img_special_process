# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/08/19
# Description : 碳星DPC真空试验稳定性数据处理
# 将动采图像分类，每图片相同位置区域求平均后输出 未进行扣本底求平均



import time
import struct
import numpy as np
import pandas as pd
import glob
from enum import Enum,unique

@unique
class enum_DPC_band(Enum):
    band_490P1 = 0
    band_490P2 = 1
    band_490P3 = 2
    band_565 = 3
    band_670P1 = 4
    band_670P2 = 5
    band_670P3 = 6
    dark_ground = 7
    band_763 = 8
    band_765 = 9
    band_865P1 = 10
    band_865P2 = 11
    band_865P3 = 12
    band_443 = 13
    band_910 = 14

# 图像宽高和平均区域
raw_info_dict = {'raw_width':512,
                'raw_height':380,
                'x1':251,
                'y1':207,
                'x2':255,
                'y2':211  
}



dir_path = 'f:\\CM真空性能测试\\试验后\\20200813T142140_CM头部真空性能测试-试验后测试'
raw_path = dir_path + '\\RAW_ImageData\\*.raw'
filelist = glob.glob(raw_path)

'''
图片取中心区域求平均
返回平均值
'''
def raw_mean(img, raw_info_dict):
    img = np.reshape(img, (raw_info_dict['raw_height'], raw_info_dict['raw_width']))
    raw_data = img[raw_info_dict['y1']:raw_info_dict['y2']+1, 
                        raw_info_dict['x1']:raw_info_dict['x2']+1]
    return round(np.mean(raw_data),2)

df_res = pd.DataFrame()

# 将文件按照波段划分 并求平均后生成15个通道的图像
# 第一层循环 ch_cnt表示图像序号 
for ch_cnt in range(1, 16): 
    img_file = list()  # 保存该通道的文件名
    # 第二层循环 遍历所有文件 找出所有第ch_cnt个通道的文件
    for filename in filelist:  
        # 生成含有该通道关键字的keyword 判断文件名是否含有该关键字
        if filename[-6] == '_' :  # 兼容 _1.raw和 01.raw
            keyword = '_' + str(ch_cnt) + '.raw'
        else:
            keyword = str(ch_cnt).zfill(2) + '.raw'
        # 该文件名属于该通道 则加入文件名列表                        
        if keyword in filename:
            img_file.append(filename)
    # 第二层循环结束 img_file中存放了所有第ch_cnt通道的图像地址

    # 读入文件 找区域平均后保存
    zone_mean = list()
    for filename in img_file:
        raw_data = np.fromfile(filename, dtype=np.uint16)
        zone_mean.append(raw_mean(raw_data, raw_info_dict))
    
    df_foo = pd.DataFrame({enum_DPC_band(ch_cnt-1).name:zone_mean})
    df_res = pd.concat([df_res, df_foo], axis=1)
    print('band' + str(ch_cnt))
# 以上 第一层循环结束

# 结果输出
now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
fout = 'vacuum-' + now + '.csv'

df_res.to_csv(fout, header=True, index=False, encoding='gbk') 
print('ok')