# -*- coding: utf-8 -*-
"""
Created on 2021.08.04

@author: Stone 
"""

import os
import sys
from module.common import (__version__, read_xml, parse_xml_to_gird)
from module.config import ReadConfig
from module.sqlite_db import HandleSqlite





if __name__ == "__main__":


    print('__version__ = ',__version__ )

    try:

        cf = ReadConfig('./config.ini')
        min_row_space = int(cf.get_val('pdf_xml','min_row_space').strip())
        min_col_space = int(cf.get_val('pdf_xml','min_col_space').strip())
        data_path = cf.get_val('pdf_xml','data_path').strip()
        output_path = cf.get_val('pdf_xml','output_path').strip()
        xml_file = cf.get_val('pdf_xml','xml_file').strip()


        xmlFilePath = os.path.abspath(os.path.join(data_path, xml_file))
        print(xmlFilePath)

        tree,root = read_xml(xmlFilePath)



        '''
        public config data for db
        '''
        db_dir = cf.get_val('sqlite_db','database_dir').strip()
        table_prefix = cf.get_val('sqlite_db','table_prefix').strip()
        table_year = cf.get_val('sqlite_db','table_year').strip()
        sql ='''INSERT INTO {0}{1} (title, value1, value2) VALUES (?, ?, ?)'''.format(table_prefix,table_year)


        '''
        合并资产负债
        '''
        print('------------------合并资产负债----------------')
        cols_rows_list = parse_xml_to_gird(root,'合并资产负债表','负债和所有者权益总计',min_row_space,min_col_space)

        '''
        insert to db
        '''
        balance_db_name = cf.get_val('sqlite_db','balance_db_name').strip()
        db_file = os.path.join(db_dir, balance_db_name)

        sqlite_handle = HandleSqlite(db_file)
        for row in cols_rows_list:
            sqlite_handle.execute_sql(sql,row) 
            sqlite_handle.close_sqlite()
        print('Insert data to Balance Success.')
        print('\r\n')



        #合并利润表
        print('------------------合并利润表----------------')
        income_db_name = cf.get_val('sqlite_db','income_db_name').strip()
        db_file = os.path.join(db_dir, income_db_name)

        sqlite_handle = HandleSqlite(db_file)

        cols_rows_list =parse_xml_to_gird(root,'合并利润表','稀释每股收益',min_row_space,min_col_space)
        for row in cols_rows_list:
            sqlite_handle.execute_sql(sql,row)
            sqlite_handle.close_sqlite()
        print('Insert data to Income sheet Success.')
        print('\r\n')





        #合并现金流量表
        print('------------------合并现金流量表----------------')
        cash_db_name = cf.get_val('sqlite_db','cash_db_name').strip()
        db_file = os.path.join(db_dir, cash_db_name)

        sqlite_handle = HandleSqlite(db_file)

        cols_rows_list =parse_xml_to_gird(root,'合并现金流量表','期末现金及现金等价物余额', min_row_space,min_col_space)
        for row in cols_rows_list:
            sqlite_handle.execute_sql(sql,row)
            sqlite_handle.close_sqlite()
        print('Insert data to Cash sheet Success.')
        print('\r\n')




    except Exception as e:  #捕获除与程序退出sys.exit()相关之外的所有异常
        print ("parse fail!",e)
        sys.exit()
