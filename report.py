# -*- coding: utf-8 -*-
"""
Created on 2021.08.04

@author: Stone 
"""

import os
import sys
from module.common import (read_xml,parse_text_box,compose_rows,compose_col)



DATAPATH = './data'
OUTPUTPATH = 'output/'
INPUT_XML = 'yanghe.pdf.xml'




if __name__ == "__main__":
    xmlFilePath = os.path.abspath(os.path.join(DATAPATH, INPUT_XML))
    print(xmlFilePath)
    try:
        tree,root = read_xml(xmlFilePath)



        #合并资产负债
        print('------------------合并资产负债----------------')

        text_list ,min_row_size = parse_text_box(root,'合并资产负债表','负债和所有者权益总计', 14)  #min_rows_size=24
        rows_list = compose_rows(text_list,  min_row_size)  #min_row_size must same with parse_text_box
        #print(rows_list)
        cols_rows_list = compose_col(rows_list)
        for row in cols_rows_list:
            print(row)




        #合并利润表
        print('------------------合并利润表----------------')

        text_list,min_row_size = parse_text_box(root,'合并利润表','稀释每股收益',14) #min_rows_size=24
        #print(text_list)

        rows_list = compose_rows(text_list, min_row_size) #min_rows_size = 60
        cols_rows_list = compose_col(rows_list,60) #min_col_size default =60
        for row in cols_rows_list:
            print(row)


    except Exception as e:  #捕获除与程序退出sys.exit()相关之外的所有异常
        print ("parse fail!",e)
        sys.exit()
