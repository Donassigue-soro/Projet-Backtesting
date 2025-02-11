import os
import sys
import backtrader as bt
from datetime import datetime
from Strategie import StrategieScalpe
import pandas as pd
import matplotlib.pyplot as plt

def backtrader_to_pandas(data):
    """Convertir un Backtrader DataFeed en Pandas DataFrame."""
    df = pd.DataFrame({
        'Datetime': [data.num2date(x) for x in range(len(data))],
        'Open': data.lines.open.get(size=len(data)),
        'High': data.lines.high.get(size=len(data)),
        'Low': data.lines.low.get(size=len(data)),
        'Close': data.lines.close.get(size=len(data)),
    })
    return df

cerebro = bt.Cerebro()

cerebro.broker.set_cash(100000)
cerebro.broker.setcommission(commission=0.001)

modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'GBPJPY.csv')

# Ajouter les données à Backtrader
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    fromdate=datetime(2024, 12, 1),
    todate=datetime(2024, 12, 28),
    timeframe=bt.TimeFrame.Minutes,
    compression=5,
    reverse=False
)
cerebro.adddata(data)

# Ajouter la stratégie
cerebro.addstrategy(StrategieScalpe)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

print('Valeur initiale du compte :', cerebro.broker.getvalue())
cerebro.run()
print('Valeur finale du compte :', cerebro.broker.getvalue())

# Convertir les données en DataFrame pour la visualisation
df_data = backtrader_to_pandas(data)

# Utiliser la classe Visualisation
visualisation = Visualisation(df_data)
visualisation.plot_candlesticks()
