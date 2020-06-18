#!/usr/bin/python
# -*- coding: utf-8 -*-
#import argparse
import requests
import json
import numpy as np
import pandas as pd
from io import StringIO


'''
parser = argparse.ArgumentParser('Option W - Website:[163, 10jqk] S - Stock,')
parser.add_argument('-w', type=str, default='163')
parser.add_argument('-s', type=int)
args = parser.parse_args()
print(args.w + ' : ' + str(args.s))
stock = str(args.s)
'''

#雪球沪深行情
stock_list = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=%s&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
'''
返回的格式如下：
{"data":{"count":3769,"list":[{"symbol":"SH603115","net_profit_cagr":25.560042709770325,"ps":null,"type":11,"percent":44.01,"has_follow":false,"tick_size":0.01,"pb_ttm":null,"float_shares":52000000,"current":14.66,"amplitude":0,"pcf":null,"current_year_percent":44.01,"float_market_capital":762320000,"market_capital":3049280000,"dividend_yield":null,"lot_size":100,"roe_ttm":20.889486452989544,"total_percent":0,"percent5m":0,"income_cagr":13.078686447016308,"amount":1018357,"chg":4.48,"issue_date_ts":1565280000000,"main_net_inflows":0,"volume":69465,"volume_ratio":null,"pb":2.502,"followers":651,"turnover_rate":0.13,"first_percent":44.01,"name":"N海星","pe_ttm":20.133,"total_shares":208000000}]},"error_code":0,"error_description":""}
'''
#雪球个股所属行业
industry = 'https://xueqiu.com/stock/industry/stockList.json?code=SZ000608&type=1&size=100'
'''
{"stockname":"","platename":"房地产","industrystocks":[{"symbol":"SZ000979","code":"000979","name":"中弘退","exchange":"SZ","current":"0.22","percentage":"4.76","change":"0.01","volume":"215311798","pe_ttm":"","marketCapital":"1.84593226378E9"}],"exchange":"CN","code":"SZ000608","industryname":"房地产"}
'''
#雪球个股信息
stock_url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=SZ000608&extend=detail'
'''
{"data":{"market":{"status_id":7,"region":"CN","status":"已收盘","time_zone":"Asia/Shanghai"},"quote":{"symbol":"SZ000608","code":"000608","high52w":7.94,"avg_price":5.949,"delayed":0,"type":11,"percent":8.67,"tick_size":0.01,"float_shares":749801859,"limit_down":5.19,"amplitude":12.48,"current":6.27,"high":6.32,"current_year_percent":27.96,"float_market_capital":4.701257656E9,"issue_date":843062400000,"low":5.6,"sub_type":"1","market_capital":4.701956447E9,"dividend":0.03,"dividend_yield":0.478,"currency":"CNY","lot_size":100,"lock_set":null,"navps":3.92,"profit":1.1464E7,"timestamp":1565334243000,"pe_lyr":410.15,"amount":2.932925065E7,"chg":0.5,"eps":0.03,"last_close":5.77,"profit_four":1.5696E7,"volume":4929945,"volume_ratio":1.82,"pb":1.599,"profit_forecast":-9.9832E7,"limit_up":6.35,"turnover_rate":0.66,"low52w":3.46,"name":"阳光股份","pe_ttm":299.564,"exchange":"SZ","pe_forecast":-42.441,"time":1565334243000,"total_shares":749913309,"open":5.78,"status":1},"others":{"pankou_ratio":-7.95},"tags":[]},"error_code":0,"error_description":""}
'''

#个股财务
finance_main = 'https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json?symbol=SZ002815&type=all&is_detail=true&count=5'
main_year = 'https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json?symbol=SZ002815&type=Q4&is_detail=true&count=5'
income = 'https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol=SZ002815&type=Q4&is_detail=true&count=5'
balance = 'https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?symbol=SZ002815&type=Q4&is_detail=true&count=5'
cash_flow = 'https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=SZ002815&type=Q4&is_detail=true&count=5'

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

'''
if args.w == '163':
    balanceSheet = bs163_year
    profit = pf163_year
    cashflow = cf163_year

if args.w == '10jqk':
    balanceSheet = bs10jqk_year
    profit = pf10jqk_year
    cashflow = cf10jqk_year
''' 

headers = {'User-Agent': 'Chrome 10'}

def getFinancialStatment(url):
    hd = {'User-Agent': 'Chrome 10'}
    res = requests.get(url, headers=hd)
    if (res.status_code == 200):
        filename = res.headers['Content-Disposition'].split()[1].split('=')[1]
        print (filename)
    return {'file': StringIO(res.text), 'name': filename}

def getStockCount():
    url = stock_list % 1
    print url
    res = requests.get(url, headers=headers)
    if (res.status_code == 200):
        stocks = json.loads(res.text)
        return stocks['data']['count']
    else:
        return 0

def getStockList(count):
    url = stock_list % count
    res = requests.get(url, headers=headers)
    if (res.status_code == 200):
        stocks = json.loads(res.text)
        return stocks['data']['list']
    else:
        return []

# 处理 资产负债表
#csv = getFinancialStatment(balanceSheet)
#report = pd.read_csv(csv.get('file'), index_col=0)
#print(report)
count = getStockCount()
print getStockList(count)


# 处理 利润表
# 处理 现金流量表
