from datetime import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
import pykrx


class SmaCross(bt.Strategy):  # bt.Strategy를 상속한 class로 생성해야 함.
    params = (
        ("period", 20),
        ("devfactor", 2),
        ("debug", False)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor, plot=True)

    def next(self):
        global size
        if not self.position:  # not in the market
            if self.data.low[0] < self.boll.lines.bot[0]:
                bottom = self.boll.lines.bot[0]
                size = int(self.broker.getcash() / bottom)  # 최대 구매 가능 개수
                self.buy(price=bottom, size=size)  # 매수 size = 구매 개수 설정
                self.log('BUY CREATE, %.2f' % (bottom))
                print(size, 'EA')
        else:
            if self.data.high[0] > self.boll.lines.mid[0]:
                self.sell(price=self.boll.lines.mid[0], size=size)  # 매도
                self.log('SELL CREATE, %.2f' % (self.boll.lines.mid[0]))
                print(size, 'EA')

list = []
with open('list.txt', 'r', encoding='UTF8') as file:
    for i in file:
        ll = [name.strip() for name in i.split(" ")]
        list.append(ll)

num = 1 # 0~43

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
#data = pykrx.stock.naver.get_market_ohlcv_by_date(fromdate=datetime(2021, 1, 1), todate=datetime(2021, 1, 1),ticker=list[num][1])
data = bt.feeds.PandasData(dataname= yf.download(list[num][1],start=datetime(2021, 1, 1), end=datetime(2023, 12, 31)))

cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print("현재 종목 : ", list[num][0])
print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style='candlestick')