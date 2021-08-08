# -*- coding: utf-8 -*-
"""
Created on 2021.08.04

@author: Stone 
"""

import os
import sys
from config import ReadConfig
from sqlite_db import HandleSqlite
from functools import reduce

'''
ROA及增长贡献分析
'''
def analyze_ROA(balance_handle, income_handle, tbname): 

    print('----------start analyze Roa --------')

    '''
    获得总资产
    '''
    vals = get_db_balance_data(balance_handle, tbname, '负债和所有者权益总计')
    '''
    print(vals)
    [(102, '负债和所有者权益总计', '3,969,611,914.85', '3,362,039,813.54')]
    '''
    if vals :
        total_asset = [float(vals[0][2].replace(',', '')), float(vals[0][3].replace(',', ''))]
        average_total_asset = round(reduce(lambda a,b : (a+b)/len(total_asset), total_asset), 2)
        YOY_total_asset = round((total_asset[0] / total_asset[1] ) - 1.0, 2)

    print('asset=',total_asset[0],total_asset[1], average_total_asset, 'YOY=',YOY_total_asset)


    '''
    获得利润表相关信息
    '''
    vals = get_db_balance_data(income_handle, tbname, '其中：营业收入')
    revenue = [float(vals[0][2].replace(',', '')), float(vals[0][3].replace(',', ''))]
    YOY_revenue = round((revenue[0] / revenue[1] ) - 1.0, 2)
    print('Revenue=',revenue[0],revenue[1], 'YOY=',YOY_revenue)

    vals = get_db_balance_data(income_handle, tbname, '其中：营业成本')
    revenue_cost = [float(vals[0][2].replace(',', '')), float(vals[0][3].replace(',', ''))]
    YOY_revenue_cost = round((revenue_cost[0] / revenue_cost[1] ) - 1.0, 2)
    print('Cost of Revenue=',revenue_cost[0],revenue_cost[1], 'YOY=',YOY_revenue_cost)


    gross_profit = [round(a -b, 2) for a,b in zip(revenue, revenue_cost)] 
    YOY_gross_profit = round((gross_profit[0] / gross_profit[1] ) - 1.0, 2)
    gross_profit_rate = [round(a/b, 3) for a, b in zip(gross_profit,revenue)]
    print('Gross Profit=',gross_profit[0], gross_profit[1], 'YOY=',YOY_gross_profit, 'Rate=',gross_profit_rate)



    print('------------end------------')


def get_db_balance_data(db_handle, tbname, title_name=None):


    if title_name :
        sql = '''select * from {0} where title = '{1}' '''.format(tbname,title_name)
    else:
        sql = 'select * from {0}'.format(tbname)

    #print(sql)

    return db_handle.search(sql)




if __name__ == '__main__':

    balance_file = '../data/database/balance_sheet.db'
    income_file = '../data/database/income_sheet.db'

    balance_handle = HandleSqlite(balance_file)
    income_handle  = HandleSqlite(income_file)
    analyze_ROA(balance_handle, income_handle, 'tb2020')





