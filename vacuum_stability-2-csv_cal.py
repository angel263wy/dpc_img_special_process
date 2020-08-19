# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/08/19
# Description : CSV文件处理 
# 用vacuum_stability-1_raw_cal.py处理完成后，将trap数据贴入文件第一列
# 本程序用所有通道的列除以第0列 得到光源修正后的灰度值 再平均值归一化

import numpy as np
import pandas as pd
import os
import glob

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
        df_foo = pd.DataFrame({'ch'+str(ch_cnt):foo})
        df_nor = pd.concat([df_nor, df_foo], axis=1)
        # 归一化
        foo_mean = foo / np.mean(foo)
        foo_mean = np.around(foo_mean, 3)
        df_foo_mean = pd.DataFrame({'ch-mean-'+str(ch_cnt):foo_mean})
        df_nor_mean = pd.concat([df_nor_mean, df_foo_mean], axis=1)
    
    # 拼接
    df_csv = pd.concat([df_csv, df_nor, df_nor_mean], axis=1)

    # 输出
    fout = 'Normal-' + filename     
    df_csv.to_csv(fout, header=True, index=False, encoding='gbk') 
    print(fout)

print('ok')

