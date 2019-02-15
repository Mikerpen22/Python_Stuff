import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.animation as animation
import datetime
from matplotlib import style
from mpl_finance import candlestick_ohlc


style.use('ggplot')

def graph_data(ticker):

    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    ########################### Parsing from api ############################

    # Fastest way to read api and load with json format
    url = 'http://www.quandl.com/api/v3/datasets/BCHARTS/{}'.format(ticker)

    # Handle some request error
    try:
        data = requests.get(url).json()  # tell the website that we want Json (otherwise you'll get html)
        arr = np.array((data['dataset']['data']))

        ohlc = []

        for append_me in arr:
            # change date str to datetime then to mdates(ohlc要的格式）
            dt = datetime.datetime.strptime(append_me[0],
                                            '%Y-%m-%d').date()  # datetime object寫回array沒用，他統一格式所以出來還是numpy.str
            date_modified = mdates.date2num(dt)
            ohlc.append(
                [date_modified, float(append_me[1]), float(append_me[2]), float(append_me[3]), float(append_me[4]),
                 float(append_me[6])])

        candlestick_ohlc(ax1, ohlc, colorup='g', colordown='r')

        # tweaking axes and annotating stuff
        for label in ax1.xaxis.get_ticklabels():  # plt.xaxis會因為如果subplot一多就抓不出誰是xaxis
            label.set_rotation(45)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 確保x軸日期格式沒變成mdates,不然跑出70000多
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))  # 決定x座標幾個標示值
        ax1.annotate('ATH', (ohlc[490][0], 19538), xytext=(0.5, 0.8), textcoords='axes fraction',
                     arrowprops=dict(facecolor='grey'))

        # Basic setup
        plt.xlabel('date')
        plt.ylabel('price')
        plt.title('BTCUSD price')
        plt.subplots_adjust(left=0.09, bottom=0.17, right=0.94, top=0.9)
        plt.show()

    except json.decoder.JSONDecodeError:
        return

graph_data('BITSTAMPUSD')
