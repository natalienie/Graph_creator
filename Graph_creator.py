import datetime
import time
import json
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.finance import candlestick_ohlc
'''
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
'''

fig = plt.figure()
ax1 = plt.subplot2grid((4,1), (0,0), rowspan=3, colspan=1)
ax2 = plt.subplot2grid((4,1), (3,0), rowspan=1, colspan=1)

def MACD(data):
    short_ave = data['close'].rolling(12).mean()
    long_ave = data['close'].rolling(26).mean()
    diff = short_ave - long_ave
    dea = diff.rolling(9).mean()
    macd = diff - dea
    return macd

def animate(i):
    '''
    dataLink = 'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_STR&start=1514815200&end=9999999999&period=300'
    '''
    data = urllib.request.urlopen('https://poloniex.com/public?command=returnChartData&currencyPair=USDT_STR&start=1514815200&end=9999999999&period=300')
    data = data.read().decode()
    data = json.loads(data)

    data = pd.DataFrame(data)

    dates = np.array(data['date'], dtype='datetime64[s]')
    data['date'] = dates
    '''
    x = 0
    y = len(data['date'])
    ohlc = []
    while x < y:
        append_me = data['date'][x], data['open'][x], data['high'][x], data['low'][x], data['close'][x]
        ohlc.append(append_me)
        x += 1

    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')


    '''
    data.set_index('date')
    macd = MACD(data)
    data['MACD'] = macd
    data.dropna(axis=0, inplace=True)
    xs = data['date'].tolist()
    ys = data['close'].tolist()
    y2s = data['MACD'].tolist()



    ax1.clear()
    ax1.plot(xs, ys, '-', label='Price')
    plt.title('STR coin Price Chart')

    ax2.plot(xs, y2s, '-')
    '''
    ax2.fill_between(xs, y2s, 0, where=(y2s > 0), facecolor='r', alpha=0.3)
    ax2.fill_between(xs, y2s, 0, where=(y2s < 0), facecolor='g', alpha=0.3)
    '''
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)


ani = animation.FuncAnimation(fig, animate, interval=60000)

plt.show()
