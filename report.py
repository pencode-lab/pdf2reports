# -*- coding: utf-8 -*-
"""
Created on 2021.08.04

@author: Stone 
"""

import os
import sys
from module.common import (__version__, read_xml, parse_xml_to_gird)
#parse_xml_to_gird(root,start_word,stop_word=None, min_row_space=16,min_col_space=60):



DATAPATH = './data'
OUTPUTPATH = 'output/'
INPUT_XML = 'zhachai.pdf.xml'




if __name__ == "__main__":


    print('__version__ = ',__version__ )

    xmlFilePath = os.path.abspath(os.path.join(DATAPATH, INPUT_XML))
    print(xmlFilePath)
    try:
        tree,root = read_xml(xmlFilePath)


        #合并资产负债
        print('------------------合并资产负债----------------')
        cols_rows_list = parse_xml_to_gird(root,'合并资产负债表','负债和所有者权益总计', min_row_space=25,min_col_space=60)
        for row in cols_rows_list:
            print(row)



        #合并利润表
        print('------------------合并利润表----------------')

        cols_rows_list =parse_xml_to_gird(root,'合并利润表','稀释每股收益', min_row_space=25,min_col_space=60)
        for row in cols_rows_list:
            print(row)

        #合并现金流量表
        print('------------------合并现金流量表----------------')
        cols_rows_list =parse_xml_to_gird(root,'合并现金流量表','期末现金及现金等价物余额', min_row_space=25,min_col_space=60)
        for row in cols_rows_list:
            print(row)



    except Exception as e:  #捕获除与程序退出sys.exit()相关之外的所有异常
        print ("parse fail!",e)
        sys.exit()
