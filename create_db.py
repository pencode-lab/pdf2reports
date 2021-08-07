# -*- coding: utf-8 -*-
"""
Created on 2021.08.04

@author: Stone 
"""

import os
import sys
import sqlite3 as lite
from module.config import ReadConfig
from module.sqlite_db import HandleSqlite




if __name__ == '__main__':


    if(True):

        cf = ReadConfig('./config.ini')
        db_dir = cf.get_val('sqlite_db','database_dir').strip()
        balance_db_name = cf.get_val('sqlite_db','balance_db_name').strip()
        income_db_name = cf.get_val('sqlite_db','income_db_name').strip()
        cash_db_name = cf.get_val('sqlite_db','cash_db_name').strip()
        table_prefix = cf.get_val('sqlite_db','table_prefix').strip()


        '''
        create balance database and table for 10 years
        '''
        db_file = os.path.join(db_dir, balance_db_name)
        sqlite_handle = HandleSqlite(db_file)

        for idx in range(2011,2021):
            tb_name = "{0}{1}test".format(table_prefix,idx)
            sql = "CREATE TABLE IF NOT EXISTS {0} (id INT PRIMARY KEY NOT NULL, title CHAR(50), value1 CHAR(50),value2 CHAR(50));".format(tb_name)
            sqlite_handle.execute_sql(sql,'')

        sqlite_handle.close_sqlite()
        print('create database {0} and tables {1}xxxx'.format(db_file,table_prefix))


        '''
        create income database and table for 10 years
        '''
        db_file = os.path.join(db_dir, income_db_name)
        sqlite_handle = HandleSqlite(db_file)

        for idx in range(2011,2021):
            tb_name = "{0}{1}".format(table_prefix,idx)
            sql = "CREATE TABLE IF NOT EXISTS {0} (id INT PRIMARY KEY NOT NULL, title CHAR(50), value1 CHAR(50),value2 CHAR(50));".format(tb_name)
            sqlite_handle.execute_sql(sql,'')

        sqlite_handle.close_sqlite()
        print('create database {0} and tables {1}xxxx'.format(db_file,table_prefix))

        '''
        create cash database and table for 10 years
        '''
        db_file = os.path.join(db_dir, cash_db_name)
        sqlite_handle = HandleSqlite(db_file)
        for idx in range(2011,2021):
            tb_name = "{0}{1}".format(table_prefix,idx)
            sql = "CREATE TABLE IF NOT EXISTS {0} (id INT PRIMARY KEY NOT NULL, title CHAR(50), value1 CHAR(50),value2 CHAR(50));".format(tb_name)
            sqlite_handle.execute_sql(sql,'')

        sqlite_handle.close_sqlite()
        print('create database {0} and tables {1}xxxx'.format(db_file,table_prefix))
        
    #end if
