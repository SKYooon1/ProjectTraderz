from datetime import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
import pykrx as stock


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f} ')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f} ')
            self.bar_executed = len(self)
        elif order.status in [order.Cancled]:
            self.log('ORDER CANCELED')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

list = []
with open('list.txt', 'r', encoding='UTF8') as file:
    for i in file:
        ll = [name.strip() for name in i.split(" ")]
        list.append(ll)

num = 42 # 0~43

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
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