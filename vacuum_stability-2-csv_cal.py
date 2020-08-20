# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/08/19
# Description : CSV文件处理 
# 用vacuum_stability-1_raw_cal.py处理完成后，将trap数据贴入文件第一列
# 特别注意 trap数据贴完后 需要保存为UTF-8格式的CSV文件
# 本程序用所有通道的列除以第0列 得到光源修正后的灰度值 再平均值归一化

import numpy as np
import pandas as pd
import os
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
    trap = 15


os.chdir('e:\\tst\\')
filelist = glob.glob('*.csv')

# 第一层循环 遍历所有文件
for filename in filelist:
    df_csv =  pd.read_csv(filename, sep=',', header=0)
    
    df_nor = pd.DataFrame()  # 保存去除光功率值
    df_nor_mean = pd.DataFrame()  # 平均值归一化
    
    # 第二层循环 遍历文件中每一列 DN值除以trap功率 对均值归一化
    for ch_cnt in range(16):
        # 每一列除以第0列 trap探测器数值 第0列输出1用于分割
        foo = np.array(df_csv.iloc[:,ch_cnt] / df_csv.iloc[:,0])
        foo = np.around(foo, 3)  # 四舍五入三位小数
        # df_foo = pd.DataFrame({'ch'+str(ch_cnt):foo})
        df_foo = pd.DataFrame({enum_DPC_band(15 if ch_cnt==0 else ch_cnt-1).name+'-DivTrap':foo})
        df_nor = pd.concat([df_nor, df_foo], axis=1)
        # 归一化
        foo_mean = foo / np.mean(foo)
        foo_mean = np.around(foo_mean-1, 3)
        df_foo_mean = pd.DataFrame({enum_DPC_band(15 if ch_cnt==0 else ch_cnt-1).name+'-norm':foo_mean})
        df_nor_mean = pd.concat([df_nor_mean, df_foo_mean], axis=1)
    
    # 拼接
    df_csv = pd.concat([df_csv, df_nor, df_nor_mean], axis=1)

    # 输出
    fout = 'Normal-' + filename     
    df_csv.to_csv(fout, header=True, index=False, encoding='gbk') 
    print(fout)

print('ok')

