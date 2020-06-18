#!/usr/bin/python
# -*- coding: utf-8 -*-
#import argparse
import requests
import json
import os, sys
import csv
import numpy as np
import pandas as pd
import ConfigParser
import operator
from io import StringIO

class InternetStocks():
    def __init__(self, headers={'User-Agent': 'Chrome 10'}):
        self.__headers = headers
        
        config = ConfigParser.ConfigParser()
        config.read('url_stock.ini')
        self.__list_url = config.get('xueqiu', 'StockList')
        self.__indicator_url = config.get('xueqiu', 'Indicator')

    def getStockCount(self):
        url = self.__list_url % 1
        res = requests.get(self.__list_url % 1, headers=self.__headers)
        if (res.status_code == 200):
            stocks = json.loads(res.text)
            return stocks['data']['count']
        else:
            return 0

    def getStockList(self):
        stock_symbol = []
        count = self.getStockCount()
        res = requests.get(self.__list_url % count, headers=self.__headers)
        if (res.status_code == 200):
            stocks = json.loads(res.text)
            detail_list = stocks['data']['list']
            for st in detail_list:
                stock_symbol.append(st['symbol'])
        return stock_symbol

    # Cycle = ['all', 'Q1', 'Q2', 'Q3', 'Q4']
    def getStockFinance(self, stock, cycle):
        url = self.__indicator_url % (stock, cycle, 3)
        headers_xueqiu = {'User-Agent': 'Chrome 10','Cookie': 'xq_a_token=17067303557fc0af0961063ffb2aa2341c3132a4'}
        res = requests.get(url, headers=headers_xueqiu)
        if (res.status_code == 200):
            return json.loads(res.text)
# end of InternetStock

class LocalStocks():
    __json_path = './allstocks/'
    def __init__(self):
        pass

    @classmethod
    def toJson(cls, name, item):
        try:
            if not os.path.exists(cls.__json_path):
                os.makedirs(cls.__json_path)
    
            with open(cls.__json_path + name, 'w') as f:
                json.dump(item, f)
                f.close()
    
        except Exception as e:
            print('write error ===> ', e)
    
    @classmethod
    def fromJson(cls, name):
        try:
            with open(cls.__json_path + name, 'r') as f:
                data = json.load(f)
                f.close()
                return data
        except Exception as e:
            print('read error ===> ', e)
        return None

    @classmethod
    def toCsv(cls, name, item):
        path = 'allstocks.csv'
        with open(path, 'a+') as wf:
            writer = csv.DictWriter(wf, fieldnames=item.keys())
            writer.writerows([item])
    
    @classmethod
    def fromCsv(cls, name):
        pass

    @classmethod
    def cacheStocks(cls):
        iStock = InternetStocks()
        stocks = iStock.getStockList()
        cls.toJson('stocklist', stocks)
        for stock in stocks:
            cls.toJson(stock, iStock.getStockFinance(stock, 'Q4'))
# end of class LocalStorage

class AnalyzeStock():
    def __init__(self):
        self.__compare = { '>': operator.gt, '<': operator.lt, '=': operator.eq, '>=': operator.ge, '<=': operator.le }
        self.__indicatores_name__map = {
            'total_revenue': '主营收入',
            'net_profit_after_nrgal_atsolc': '扣非净利润',
            'np_atsopc_nrgal_yoy': '扣非净利润增长率',
            'operating_income_yoy': '营收同比增长',
            'gross_selling_rate': '毛利率',
            'net_selling_rate': '净利率',
            'net_interest_of_total_assets': '总资产收益率',
            'avg_roe': '净资产收益率',
            'ore_dlt': '净资产收益率-摊薄',
            'operate_cash_flow_ps': '每股现金流',
        }
        self.__indicators_map = {
            '主营收入': 'total_revenue',
            '扣非净利润': 'net_profit_after_nrgal_atsolc',
            '扣非净利润增长率': 'np_atsopc_nrgal_yoy',
            '营收同比增长': 'operating_income_yoy',
            '毛利率': 'gross_selling_rate',
            '净利率': 'net_selling_rate',
            '总资产收益率': 'net_interest_of_total_assets',
            '净资产收益率': 'avg_roe',
            '净资产收益率-摊薄': 'ore_dlt',
            '每股现金流': 'operate_cash_flow_ps',
        }
        self.expected_stocks = {}

    def getStockIndicatores(self, stock):
        indicatores = LocalStocks.fromJson(stock)
        return indicatores['data']['list']
    
    def financeFilter(self, filters, finances):
        if not finances or len(finances) < 3:
            return False
    
        for item in filters:
            match = item.split()
            name = self.__indicators_map[match[0]]
            op = match[1]
            expectation = float(match[2])
    
            for finance in finances:
                value = finance[name][0]
                if not self.__compare[op](value, expectation):
                    return False
        return True
    
    def analyzeStock(self, conditions):
        self.expected_stocks.clear()
        stocks = LocalStocks.fromJson('stocklist')
        if (stocks is None):
            print('Error: Stocks not cached')
            return {}
        i = 0
        for stock in stocks:
            finances = self.getStockIndicatores(stock)
            if (self.financeFilter(conditions, finances)):
                self.expected_stocks[stock] = finances
                i = i + 1
        print ('total: ', i)
        return self.expected_stocks
# end of class analyzeStock
        
def main():
    if (len(sys.argv) > 1 and sys.argv[1] == 'cache'):
        LocalStocks.cacheStocks()
    else:
        analyzer = AnalyzeStock()
        res = analyzer.analyzeStock(['毛利率 > 30', '净利率 > 10', '净资产收益率 > 10', '每股现金流 > 0.5', '扣非净利润增长率 > 5'])
        print (res.keys())

# 处理 资产负债表
#csv = getFinancialStatment(balanceSheet)
#report = pd.read_csv(csv.get('file'), index_col=0)
#print(report)
#getStockIndicatores('SZ300331', 3, 'Q4')
#getStockIndicatores('SZ300332', 3, 'Q4')
#getAllStocks()
#getStockIndicatores('SZ300331')

# 处理 利润表
# 处理 现金流量表
if __name__ == '__main__':
    main()
