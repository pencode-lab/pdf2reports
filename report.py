# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:50:51 2017

@author: mkonrad
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
        text_list = parse_text_box(root,'合并资产负债表','负债和所有者权益总计',20)


        rows_list = compose_rows(text_list, 20)
        #print(rows_list)

        cols_rows_list = compose_col(rows_list)
        for row in cols_rows_list:
            print(row)

    except Exception as e:  #捕获除与程序退出sys.exit()相关之外的所有异常
        print ("parse fail!",e)
        sys.exit()
