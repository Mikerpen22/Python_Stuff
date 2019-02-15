import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc

import urllib.request
import datetime as dt
import re

bad_pattern = re.compile(r'[a-zA-Z]+')


# 你要處理資料中日期的那一列，把他從str timestamp轉成mdate看得懂的timestamp（python3改成這鳥樣）
def bytespdate2num(fmt, encoding='utf-8'):
    strConverter = mdates.strpdate2num(fmt)  # create一個converter把'%Y-%m-%d'轉成我要的timestamp(只有跑第一次)

    def bytesConverter(b):  # 把bytes decode成str
        s = b.decode(encoding)
        return strConverter(s)      # 這其實才是我要return的東西
    return bytesConverter  # 我沒加（）--> 代表回傳的是一個bytesConverter的reference


def graph_data(stock_name):

    fig = plt.figure()  # Define figure
    ax1 = plt.subplot2grid((1, 1), (0, 0))   # Define axes; ((shape),(starting point))

    # Define Data
    stock_price_url = 'https://pythonprogramming.net/yahoo_finance_replacement'
    source_code = urllib.request.urlopen(stock_price_url).read().decode()  # 加decode不然會跑出byte
    stock_data = []
    split_source = source_code.split('\n')
    for aline in split_source:
        if re.match(bad_pattern, aline) is None:  # 有英文字的就不是我要的東西
            stock_data.append(aline)

    '''用numpy把stock_data裡的string讀成變數
       arguement的converters是要把日期從原本的timestamp轉成matplotlib看得懂的形式（一般來說會用unix time)
       這個bytespdate2num實際上只run一次（有點像用來initialize，之後都連到bytesConverter去了）'''
    date, openp, highp, lowp, closep, adjusted_closep, volume = np.loadtxt(stock_data,
                                                                           delimiter=',',
                                                                           unpack=True,
                                                                           converters={0: bytespdate2num('%Y-%m-%d')})

    '''if data contains unix time we don't need converter:
    dateConv = np.vectorize(dt.datetime.fromtimestamp)
    date = dateConv(date)'''

####################################### Plot with line ##########################################
    # def line_Chart(d, p):
    #     ax1.plot_date(d, p, '-', label='price')
    #     for label in ax1.xaxis.get_ticklabels():  # plt.xaxis會因為如果subplot一多就抓不出誰是xaxis
    #         label.set_rotation(45)
    #         label.set_color('red')
    #     ax1.grid(True)
    #     ax1.spines['right'].set_visible(False)  # 除了x,y軸其他弄掉
    #     ax1.spines['top'].set_visible(False)
    #     ax1.set_yticks(range(0, 200, 25))  # 設定y軸要有那些值
    #     ax1.set_ylim(bottom=0)  # y=0不會往上跑
    #     ax1.fill_between(d, p, 0, alpha=0.2)

    # line_Chart(date, adjusted_closep)

####################################### Plot with OHLC ##########################################

    ohlc = []
    arr = np.array([date, openp, highp, lowp, adjusted_closep, volume])
    for a_set in arr.T:
        ohlc.append(a_set)
    candlestick_ohlc(ax1, ohlc)

    plt.xlabel('date')
    plt.ylabel('price')
    plt.title('Stock Plotting Practice')
    plt.legend(stock_name)
    plt.subplots_adjust(left=0.09, bottom=0.17, right=0.94, top=0.9)
    plt.show()


graph_data('TSLA')
