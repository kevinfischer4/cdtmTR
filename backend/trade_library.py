import pandas as pd
import vectorbt as vbt

# 1) Transaktionen laden
tx = pd.read_sql("SELECT * FROM transactions WHERE user_id = %s", con=engine, params=[user_id], index_col='executed_at', parse_dates=['executed_at'])

# 2) Einmal alle ISINs extrahieren
isins = tx['isin'].unique()

# 3) Kursdaten laden (automatisch via yfinance)
#    Dictionary: ISIN → Ticker-Mapping (hier Dummy-Beispiel)
isin_to_ticker = {
    'DE0008469008': 'DAX',       # Beispiel ISIN → Yahoo Ticker
    'US0378331005': 'AAPL',
    # weitere Zuordnungen ...
}
tickers = [isin_to_ticker[isin] for isin in isins]
price_data = vbt.YFData.download(tickers, start='2020-01-01').get('Close')

# 4) Portfolio aus Transaktionen erstellen
#    Gruppieren pro ISIN und in Portfolio übertragen
portfolio = vbt.Portfolio.from_orders(
    close=price_data,
    size=pd.Series(tx['size'].values, index=tx.index),
    price=pd.Series(tx['price'].values, index=tx.index),
    fees=pd.Series(tx['fee'].values, index=tx.index),
    group_by=tx['isin'].values,     # Gruppiere Orders nach ISIN
    accumulate=True,
    freq='1D'
)

# 5) Aktuelle Positionen abrufen
# → Letzter Eintrag der "positions"-Tabelle
positions = portfolio.positions.iloc[-1]

# 6) Ausgabe der aktuellen Bestände (ISIN + Stückzahl)
isin_positionen = dict(zip(isins, positions.values))
print("Aktuelle Positionen im Portfolio:")
for isin, qty in isin_positionen.items():
    print(f"ISIN: {isin}, Stückzahl: {qty:.2f}")

# 7) Risiko-Kennzahlen berechnen
volatility = portfolio.annualized_volatility()
sharpe = portfolio.sharpe_ratio()
max_drawdown = portfolio.max_drawdown()
var_95 = portfolio.value_at_risk(confidence_level=0.95)
beta = portfolio.beta()

print("\nKennzahlen:")
print(f"Volatilität (1J): {volatility:.2%}")
print(f"Sharpe-Ratio: {sharpe:.2f}")
print(f"Max Drawdown: {max_drawdown:.2%}")
print(f"VaR 95%: {var_95:.2%}")
print(f"Beta: {beta:.2f}")