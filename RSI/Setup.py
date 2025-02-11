import os.path  # To manage paths
import sys  
import backtrader as bt
from datetime import datetime
from Scalping import SimpleSmaCrossoverStrategy  # Assurez-vous que ce module est accessible

# Configuration de Cerebro
cerebro = bt.Cerebro()

# Capital initial
cerebro.broker.set_cash(1000000)

modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'EURUSD.csv')
# Chargement des données
data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,  # Vérifiez que le chemin est correct
        fromdate=datetime(2020, 11, 21),  # Date de début
        todate=datetime(2024, 12, 15),    # Date de fin
        
        reverse=False,
        dtformat='%Y-%m-%d',  # Format des dates dans le fichier CSV
        openinterest=-1  # Si la colonne openinterest est absente ou non utilisée, indiquez -1
)

cerebro.adddata(data)

# Ajout de la stratégie
cerebro.addstrategy(SimpleSmaCrossoverStrategy)

# Ajout d'un sizer de taille fixe selon le montant investi
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

# Afficher la valeur initiale du portefeuille
print('Valeur de départ du portefeuille : %.2f' % cerebro.broker.getvalue())

# Exécution de Cerebro
cerebro.run()

# Afficher la valeur finale du portefeuille
print('Valeur finale du portefeuille : %.2f' % cerebro.broker.getvalue())

# Tracer les résultats avec un style en chandelier
cerebro.plot()