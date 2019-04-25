#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import argparse
import numpy as np
import pandas as pd
from io import StringIO

parser = argparse.ArgumentParser('Option W - Website:[163, 10jqk] S - Stock,')
parser.add_argument('-w', type=str, default='163')
parser.add_argument('-s', type=int)
args = parser.parse_args()
print(args.w + ' : ' + str(args.s))
stock = str(args.s)

# 同花顺数据，excel格式
bs10jqk_year = 'http://basic.10jqka.com.cn/api/stock/export.php?export=debt&type=year&code=' + stock
bs10jqk = 'http://basic.10jqka.com.cn/api/stock/export.php?export=debt&type=simple&code=' + stock
pf10jqk_year = 'http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=year&code=' + stock
pf10jqk = 'http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=simple&code=' + stock
cf10jqk_year= 'http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=year&code=' + stock
cf10jqk_year= 'http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=simple&code=' + stock

# 网易数据，和新浪的相同，但是提供数据下载，csv格式
bs163 = 'http://quotes.money.163.com/service/zcfzb_' + stock + '.html'
bs163_year = 'http://quotes.money.163.com/service/zcfzb_' + stock + '.html?type=year'
pf163 = 'http://quotes.money.163.com/service/lrb_' + stock + '.html'
pf163_year = 'http://quotes.money.163.com/service/lrb_' + stock + '.html?type=year'
cf163 = 'http://quotes.money.163.com/service/xjllb_' + stock + '.html'
cf163_year = 'http://quotes.money.163.com/service/xjllb_' + stock + '.html?type=year'

if args.w == '163':
    balanceSheet = bs163_year
    profit = pf163_year
    cashflow = cf163_year

if args.w == '10jqk':
    balanceSheet = bs10jqk_year
    profit = pf10jqk_year
    cashflow = cf10jqk_year
    

def getFinancialStatment(url):
    hd = {'User-Agent': 'Chrome 10'}
    res = requests.get(url, headers=hd)
    if (res.status_code == 200):
        filename = res.headers['Content-Disposition'].split()[1].split('=')[1]
        print (filename)
    return {'file': StringIO(res.text), 'name': filename}

# 处理 资产负债表
csv = getFinancialStatment(balanceSheet)
report = pd.read_csv(csv.get('file'), index_col=0)
print(report)


# 处理 利润表
# 处理 现金流量表
