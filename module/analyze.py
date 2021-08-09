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



def __get_balance_col_val(handle, tbname, title):
    this_year_val = 0.0
    prev_year_val = 0.0
    yoy = 0.0

    vals = get_db_data(balance_handle, tbname, title)[0]
    if vals and len(vals)==4:
        this_year_val = float(vals[2].replace(',', ''))
        prev_year_val =  float(vals[3].replace(',', ''))
        yoy = this_year_val / prev_year_val - 1.0


    return this_year_val, prev_year_val, yoy



def __get_income_col_val(handle, tbname, title):
    this_year_val = 0.0
    prev_year_val = 0.0
    yoy = 0.0

    vals = get_db_data(handle, tbname, title)[0]
    if vals and len(vals)==4:
        this_year_val = float(vals[2].replace(',', ''))
        prev_year_val =  float(vals[3].replace(',', ''))
        yoy = this_year_val / prev_year_val  - 1.0

    return this_year_val, prev_year_val, yoy






def analyze_ROA(balance_handle, income_handle, tbname): 

    search_income_titles =('营业收入', '营业成本', '税金及附加', '销售费用', '管理费用', '研发费用',
            '财务费用', '营业利润', '利润总额', '所得税费用','净利润' )


    print('----------start analyze Roa --------')

    '''
    获得总资产
    '''


    title = '负债和所有者权益总计'
    t_total_asset, p_total_asset, YOY_total_asset =  __get_balance_col_val(balance_handle,tbname, title)
    average_total_asset  = (t_total_asset + p_total_asset)/2 
    print('asset=',t_total_asset, p_total_asset, average_total_asset, 'YOY=',YOY_total_asset)


    '''
    获得利润表相关信息
    '''
    income_values=[] #[title, this_year_value, prev_year_value, yoy, contribution,income_ratio,roa_ratio ]
    for title in search_income_titles:
        t, p, yoy = __get_income_col_val(income_handle,tbname, title)
        contribution = yoy #contribution default is yoy
        income_values.append([title, t, p, yoy, contribution])





    '''Renenue'''
    revenue_title = '营业收入'
    revenue_cost_title = '营业成本'


    revenue = list(filter(lambda x: x[0] == revenue_title, income_values))[0]
    revenue_cost =list(filter(lambda x: x[0] == revenue_cost_title, income_values))[0]

    gropss_profit =list(map( lambda x : x[0] - x[1], zip(revenue[1:3],revenue_cost[1:3]) ))
    yoy_gropss_profit = gropss_profit[0] / gropss_profit[1] -1
    gropss_profit = ['毛利润',gropss_profit[0],gropss_profit[1], yoy_gropss_profit ]
    income_values.append(gropss_profit)
    
    gropss_profit_rate = list(map( lambda x : x[1] / x[0], zip(revenue[1:3],gropss_profit[1:3]) ))
    yoy_gropss_profit_rate = gropss_profit_rate[0] / gropss_profit_rate[1] -1
    gropss_profit_rate = ['毛利率',gropss_profit_rate[0],gropss_profit_rate[1], yoy_gropss_profit_rate ]
    income_values.append(gropss_profit_rate)

    '''营业成本 = 税金及附加 + 销售费用 + 管理费用 + 研发费用 +财务费用 '''

    tmp_list = zip( 
                list(filter(lambda x: x[0] == '税金及附加', income_values))[0][1:3],
                list(filter(lambda x: x[0] == '销售费用', income_values))[0][1:3], 
                list(filter(lambda x: x[0] == '管理费用', income_values))[0][1:3], 
                list(filter(lambda x: x[0] == '研发费用', income_values))[0][1:3],
                list(filter(lambda x: x[0] == '财务费用', income_values))[0][1:3]
                )

    tmp_list = list(tmp_list)
    operating_cost = ['运营成本',reduce(lambda a, b: a + b, tmp_list[0]), reduce(lambda a, b: a + b, tmp_list[1])]
    yoy_operating_cost = operating_cost[1]/operating_cost[2] -1
    operating_cost.append(yoy_operating_cost)
    income_values.append(operating_cost)


    '''其他营业收入 = 营业利润 - (毛利 - 运营成本)'''
    operating_profit = list(filter(lambda x: x[0] == '营业利润', income_values))[0]
    other_operating_cost =[ '其他营业收入',
            operating_profit[1] - ( gropss_profit[1] -operating_cost[1]),
            operating_profit[2] - ( gropss_profit[2] -operating_cost[2]),
            (operating_profit[1] - ( gropss_profit[1] -operating_cost[1]))/(operating_profit[2] 
                    - ( gropss_profit[2] -operating_cost[2])) -1
        ]

    income_values.append(other_operating_cost)


    '''营业外收入 = 利润总额 - 营业利润'''
    profit_before_tax = list(filter(lambda x: x[0] == '利润总额', income_values))[0]
    non_operating_profit = [ '营业外收入',
            profit_before_tax[1] - operating_profit[1],
            profit_before_tax[2] - operating_profit[2],
            (profit_before_tax[1] - operating_profit[1])/( profit_before_tax[2] - operating_profit[2]) -1
            ] 
    income_values.append(non_operating_profit)

    '''
    处理增长贡献度数据
    '''
    revenue_cost[3] = (gropss_profit[3] - revenue[3])
    operating_cost[3] = (operating_profit[3] - gropss_profit[3] )
    non_operating_profit[3] = (profit_before_tax[3] - operating_profit[3])

    #所得税
    income_tax = list(filter(lambda x: x[0] == '所得税费用', income_values))[0]
    net_profit = list(filter(lambda x: x[0] == '净利润', income_values))[0]
    income_tax[3] =( net_profit[3] - profit_before_tax[3])



    '''占比处理（占营业收入的比例）'''
    this_year_revenue_val = revenue[1]
    for row in income_values:
        row.append(row[1]/this_year_revenue_val)


    ''''处理ROA分解'''
    for row in income_values:
        row.append(row[1]/average_total_asset)



    print('项目 | 当年数值 | 上一年数值 | 同比 | 增长贡献度 | 占比 | ROA占比')
    print('-------------------------------------------------------------')
    for x in income_values: 
        print(x)
        
    print('------------end------------')


def get_db_data(db_handle, tbname, title_name=None):


    if title_name :
        sql = '''select * from {0} where title like '%{1}%' '''.format(tbname,title_name)
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





