import backtrader as bt

class SimpleSmaCrossoverStrategy(bt.Strategy):
    params = (
        ("sma_short", 10),  # SMA courte
        ("sma_long", 20),   # SMA longue
    )

    def __init__(self):
        # Initialiser les indicateurs
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_short)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_long)

    def next(self):
        # Vérifier qu'il y a suffisamment de données pour les calculs
        if len(self.data) < max(self.params.sma_short, self.params.sma_long):
            print(f"Pas assez de données pour effectuer les calculs (len(data)={len(self.data)})")
            return

        # Vérifier si nous avons déjà une position
        if self.position:
            # Condition de sortie : le prix passe sous la SMA courte
            if self.data.close[0] < self.sma_short[0]:
                print("Sortie de position - Vente déclenchée")
                self.close()
                return

        # Condition d'achat
        if self.sma_short[0] > self.sma_long[0] and self.data.close[0] > self.sma_short[0]:
            print("Achat déclenché")
            self.buy()

        # Condition de vente
        elif self.sma_short[0] < self.sma_long[0] and self.data.close[0] < self.sma_short[0]:
            print("Vente déclenchée")
            self.sell()
