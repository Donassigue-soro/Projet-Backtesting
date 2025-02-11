import yfinance as yf

# Télécharger les données historiques pour Microsoft
data = yf.download('MSFT', start='2011-01-01', end='2012-12-31')

# Enregistrer les données dans un fichier CSV
data.to_csv('MSFT_data.csv')

print("Données téléchargées et enregistrées dans MSFT_data.csv")
