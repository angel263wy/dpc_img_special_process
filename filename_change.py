# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2020/09/15
# Description : 


import glob
import os 

path = 'f:\\shuju\\'
os.chdir(path)
dirs = glob.glob('*')  


for dir in dirs:  # dir字符串范例: 20200907T181849_02-全视场GMI球-P001
    print(dir)
    fov_cnt = dir[-4:]  # 获取视场角编号
    
    pathsave = os.getcwd()  # 工作目录备份
    os.chdir(path + '\\' + dir + '\\RAW_ImageData')
    
    oldnames = glob.glob('*.raw')
        
    for oldname in oldnames:  # raw_file保存了RAW_ImageData中所有raw文件
        newname = fov_cnt + '_' + oldname
        os.rename(oldname, newname)
        # print(oldname,'======>',newname)    
    
    os.chdir(pathsave)  # 工作目录恢复