import backtrader as bt

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Fonction de logging pour cette stratégie '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=14)  # SMA à 14 périodes
        self.buy_signals = []  # Pour stocker les signaux d'achat
        self.sell_signals = []  # Pour stocker les signaux de vente

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Achat exécuté, %.2f' % order.executed.price)
                self.buy_signals.append((self.datas[0].datetime.date(0), order.executed.price))
            elif order.issell():
                self.log('Vente exécutée, %.2f' % order.executed.price)
                self.sell_signals.append((self.datas[0].datetime.date(0), order.executed.price))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Ordre annulé/marge insuffisante/rejeté')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'Trade clôturé - PnL: {trade.pnl:.2f}')

    def next(self):
        self.log('Clôture, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:  # Achat si prix > SMA
                self.log('ACHAT CRÉÉ, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0] and len(self) >= self.bar_executed + 5:  # Vente avec délai
                self.log('VENTE CRÉÉE, %.2f' % self.dataclose[0])
                self.order = self.sell()
