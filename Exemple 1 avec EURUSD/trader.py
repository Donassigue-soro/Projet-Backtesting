import backtrader as bt
import pandas as pd
import plotly.graph_objects as go
from strategies import TestStrategy  # Import de la stratégie

# Chargement des données
file_path = 'Exemple 1 avec EURUSD/EURUSD.csv'
data = pd.read_csv(file_path)

# Conversion de la colonne 'Date' en datetime
data['Date'] = pd.to_datetime(data['Date'])

# Préparation des données pour Backtrader
dataframe = data[['Date', 'Open', 'High', 'Low', 'Close']]
dataframe.rename(columns={'Date': 'datetime', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}, inplace=True)

# Backtrader setup
cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000000)

bt_data = bt.feeds.PandasData(
    dataname=dataframe,
    datetime='datetime',
    open='open',
    high='high',
    low='low',
    close='close',
    volume=None
)
cerebro.adddata(bt_data)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

# Exécution de la stratégie
result = cerebro.run()
strategy = result[0]  # Récupération de l'instance de la stratégie

# Récupération des signaux d'entrée/sortie
buy_signals = strategy.buy_signals
sell_signals = strategy.sell_signals


# Création du graphique en chandeliers avec Plotly
fig = go.Figure(data=[go.Candlestick(
    x=dataframe['datetime'],
    open=dataframe['open'],
    high=dataframe['high'],
    low=dataframe['low'],
    close=dataframe['close'],
    name='EURUSD'
)])

# Ajout des points d'entrée (achat)
for signal in buy_signals:
    fig.add_trace(go.Scatter(
        x=[signal[0]],
        y=[signal[1]],
        mode='markers',
        marker=dict(color='green', size=10),
        name='Achat'
    ))

# Ajout des points de sortie (vente)
for signal in sell_signals:
    fig.add_trace(go.Scatter(
        x=[signal[0]],
        y=[signal[1]],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Vente'
    ))

# Personnalisation du graphique
fig.update_layout(
    title='Graphique EURUSD avec points d\'entrée et sortie',
    xaxis_title='Date',
    yaxis_title='Prix',
    xaxis_rangeslider_visible=False
)

fig.show()
