import pandas as pd
import requests
import vectorbt as vbt
import yfinance as yf
from data_loader import load_banking_data, load_trading_data
import os
import pandas as pd
import vectorbt as vbt
from data_loader import load_banking_data, load_trading_data
from model import Trade, Risk  # Make sure your models are imported
import os
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

# --- Konfiguration ---
OPENFIGI_API_KEY = 'f2f77183-a421-412f-95e2-8639b600f895'  # Ersetze durch deinen OpenFIGI API-Schlüssel
USER_ID = '36fd51ee-dadd-45ee-8577-5a6688463abc'           # Ersetze durch die gewünschte Benutzer-ID

# --- 1. Transaktionsdaten laden ---
# Beispiel: Lade Transaktionen aus einer CSV-Datei
# Du kannst diesen Teil anpassen, um Daten aus deiner Datenbank zu laden
# Lade alle Trades
trade_data = load_trading_data(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data.csv"))

    # 🔸 Filter auf Benutzer
trade_data = [trade for trade in trade_data if getattr(trade, "user_id", None) == USER_ID]
trade_data = pd.DataFrame(trade_data)

# --- 2. ISINs extrahieren ---
unique_isins = trade_data['ISIN'].unique().tolist()

# --- 3. ISIN zu Ticker-Mapping über OpenFIGI ---
def map_isins_to_tickers(isins):
    headers = {
        'Content-Type': 'application/json',
        'X-OPENFIGI-APIKEY': OPENFIGI_API_KEY
    }
    mappings = [{'idType': 'ID_ISIN', 'idValue': isin} for isin in isins]
    response = requests.post('https://api.openfigi.com/v3/mapping', headers=headers, json=mappings)
    response.raise_for_status()
    data = response.json()
    isin_ticker_map = {}
    for item in data:
        isin = item.get('data', [{}])[0].get('idValue', None)
        ticker = item.get('data', [{}])[0].get('ticker', None)
        if isin and ticker:
            isin_ticker_map[isin] = ticker
    return isin_ticker_map

isin_to_ticker = map_isins_to_tickers(unique_isins)

trade_data['Ticker'] = trade_data['ISIN'].map(isin_to_ticker)

# Entferne Zeilen ohne Ticker
trade_data.dropna(subset=['Ticker'], inplace=True)

# Korrekt: Auswahl von Spalten
print(trade_data[['ISIN', 'Ticker']])

