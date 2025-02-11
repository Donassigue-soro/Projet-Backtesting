import backtrader as bt

class StrategieScalpe(bt.Strategy):
    
    params = (
        ('sma_short_period', 20),  # Période de la SMA courte
        ('sma_long_period', 50),  # Période de la SMA longue
        ('rsi_period', 7),        # Période du RSI
        ('bollinger_period', 20), # Période des Bandes de Bollinger
        ('bollinger_dev', 2),     # Facteur de déviation des Bandes de Bollinger
        ('atr_period', 14),       # Période de l'ATR
    )
    
    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()} {txt}')
        
    
    def __init__(self):
       
        # Moyennes mobiles simples
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_long_period)

        # RSI
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

        # Bandes de Bollinger
        self.bollinger = bt.indicators.BollingerBands(self.data.close, 
                                                    period=self.params.bollinger_period, 
                                                    devfactor=self.params.bollinger_dev)

        # ATR
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
    
    def next(self):
        # Variables utiles
        sma_short = self.sma_short[0]
        sma_long = self.sma_long[0]
        rsi = self.rsi[0]
        price = self.data.close[0]
        lower_band = self.bollinger.lines.bot[0]
        upper_band = self.bollinger.lines.top[0]
        atr = self.atr[0]  # Volatilité basée sur l'ATR

        # *** Conditions d'Achat ***
        if not self.position:  # Pas de position ouverte
            if sma_short > sma_long and \
            rsi > 20 and self.rsi[-1] <= 20 and \
            price <= lower_band:
                # Achat
                stop_loss = price - (2 * atr)  # Stop-loss basé sur l'ATR
                take_profit = price + (4 * atr)  # Take-profit au ratio 1:2
                
                self.buy(size=1)  # Acheter une unité
                self.log(f'BUY: {price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}')
                
                # Enregistrer les niveaux de sortie
                self.stop_loss = stop_loss
                self.take_profit = take_profit

        # *** Conditions de Vente ***
        elif not self.position:
            if sma_short < sma_long and \
            rsi > 80 and self.rsi[-1] >= 80 and \
            price >= upper_band:
                # Vente
                stop_loss = price + (2 * atr)  # Stop-loss basé sur l'ATR
                take_profit = price - (4 * atr)  # Take-profit au ratio 1:2
                
                self.sell(size=1)  # Vendre une unité
                self.log(f'SELL: {price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}')
                
                # Enregistrer les niveaux de sortie
                self.stop_loss = stop_loss
                self.take_profit = take_profit

        # *** Sortie de Position (Stop Loss / Take Profit) ***
        if self.position:
            if self.position.size > 0:  # Position d'achat
                if price <= self.stop_loss or price >= self.take_profit:
                    self.close()  # Fermer la position
                    self.log(f'CLOSE LONG: {price}')

            elif self.position.size < 0:  # Position de vente
                if price >= self.stop_loss or price <= self.take_profit:
                    self.close()  # Fermer la position
                    self.log(f'CLOSE SHORT: {price}')
