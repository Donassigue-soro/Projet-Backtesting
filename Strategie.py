import backtrader as bt

class StrategiePriceAction(bt.Strategy):
    params = dict(
        risk_gain = 2.0  # ration risque/gain
        atr_mult = 1.5   # Multiplicateur ATR pour definir le SL
        fvg_periode = 3            # Peridode pour detecter les faire value gaps
        trailing_atr  1.0          # Multiplicateur ATR pour le trailling stop
        ema_periode = 50           # Filtré les tendance avec l'EMA
        rsi_periode = 14           # RSI pour confirmé les entrées
        rsi_surachat = 70
        rsi_survente = 30
    )
    # Initialisation des indicateur techniques
    def _init_(self):
        self.atr = bt.indicator.ATR( periode = 14)  #Volatillité pour SL
        self.ema = bt.indicator.ExponentialMovingAverage( period= self.p.ema_periode)   #filtre les tendances
        self.rsi = bt.indicator.RSI( period= self.p.rsi_periode)
        self.highest = bt.indicators.Highest(self.data.high, period=20)  # HH
        self.lowest = bt.indicators.Lowest(self.data.low, period=20)  # LL
        self.sma_volume = bt.indicator.SMA(self.data.volume, period=20)
   
   # Détecter les FAIR VALUE GAPS basé sur 3 bougies
   
   def detecte_fvg(self):
        if self.data.low[-2] > self.data.high[0]:
            return "Haussier"
        if self.data.high[-2] < self.data.low[0]:
            return "Baissier"
        return None
        
    # Détecter les changement de structure BOS/CHoCH
    
    def detecte_ChangementDeStructure(self): 
        prev_high = self.highest[-1]
        prev_low = self.lowest[-1]
        
        if self.data.close[0] > prev_high :
            return "BOS_haussier"
        if self.data.close[0] < prev.low
            return "BOS_baissier"
    
    # Détecter un stop en regardant si le prix depasse un HH/LL avant de revenir
    
    def detecte_liquidite_grap(self) :
        prev_high = self.highest[1]
        prev_low = self.lowest[-1]
        
        if self.data.close.high[0] > prev_high and self.data.close[0] < prev_high :
            return "liquidite_baissiere"
        elif self.data.close[0] < prev_low and elf.data.close[0] < prev_low:
            return "liquiditer_baissier"
        return None
        
    def next(self) :
       if self.position:
            sl = self.data.close[0] - self.atr[0] * self.p.trailing_atr if self.position.size > 0 else self.data.close[0] + self.atr[0] * self.p.trailing_atr
            self.sell(size=self.position.size, exectype=bt.Order.Stop, price=sl) if self.position.size > 0 else self.buy(size=-self.position.size, exectype=bt.Order.Stop, price=sl)
            return
            
        fvg = self.detecte_fvg()
        Changement_De_structure = self.ChangementDeStructure
        liquidity_grab = self.detecte_liquidite_grap
        high_volume = self.data.volume[0] > self.volume_sma[0]
        above_ema = self.data.close[0] > self.ema[0]  # Contexte haussier
        below_ema = self.data.close[0] < self.ema[0]  # Contexte baissier
        
        # Stratégie d'achat
        if fvg == "bullish" and Changement_De_structure == "BOS_BULLISH" and liquidity_grab == "liquidity_sweep_bullish" and high_volume and above_ema and self.rsi[0] < self.p.rsi_oversold:
            sl = self.data.low[0] - self.atr[0] * self.p.atr_mult
            tp = self.data.close[0] + (self.data.close[0] - sl) * self.p.risk_reward
            self.buy(size=1, exectype=bt.Order.Market)
            self.sell(size=1, exectype=bt.Order.Stop, price=sl)
            self.sell(size=1, exectype=bt.Order.Limit, price=tp)

        # Stratégie de vente
        elif fvg == "bearish" and Changement_De_structure == "BOS_BEARISH" and liquidity_grab == "liquidity_sweep_bearish" and high_volume and below_ema and self.rsi[0] > self.p.rsi_overbought:
            sl = self.data.high[0] + self.atr[0] * self.p.atr_mult
            tp = self.data.close[0] - (sl - self.data.close[0]) * self.p.risk_reward
            self.sell(size=1, exectype=bt.Order.Market)
            self.buy(size=1, exectype=bt.Order.Stop, price=sl)
            self.buy(size=1, exectype=bt.Order.Limit, price=tp)


            
