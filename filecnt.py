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
    # print(dir)    
    filelist = glob.glob(dir + '\\RAW_ImageData\\*.raw')
    cnt = len(filelist)
    if cnt == 149:
        print(f'{dir} 文件数量正确')
    else:
        print(f'{dir} 文件数量错误 实际数量为{cnt}')
    

