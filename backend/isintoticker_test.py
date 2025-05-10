import pandas as pd
import yfinance as yf

# --- Konfiguration ---
INPUT_CSV_PATH = r"C:\Users\cmgue\Downloads\trading_sample_data.csv"  # Pfad zur Eingabedatei
OUTPUT_CSV_PATH = r"C:\Users\cmgue\Downloads\trading_sample_data - Copy.csv"  # Pfad zur Ausgabedatei

# --- 1. Transaktionsdaten aus CSV laden ---
print(f"Lade Transaktionsdaten aus {INPUT_CSV_PATH}...")
try:
    trade_data = pd.read_csv(INPUT_CSV_PATH)
    print("Transaktionsdaten erfolgreich geladen.")
except FileNotFoundError:
    print(f"Fehler: Datei {INPUT_CSV_PATH} nicht gefunden.")
    exit()

# Debug: Zeige die ersten Zeilen der Transaktionsdaten
print("Vorschau der Transaktionsdaten:")
print(trade_data.head())

# --- 2. ISINs extrahieren ---
if 'ISIN' not in trade_data.columns:
    print("Fehler: Die Spalte 'ISIN' fehlt in der Eingabedatei.")
    exit()

unique_isins = trade_data['ISIN'].unique().tolist()
print(f"Gefundene eindeutige ISINs: {len(unique_isins)}")

# --- 3. ISIN zu Yahoo Finance-Ticker-Mapping ---
def map_isins_to_yahoo_tickers(isins):
    isin_ticker_map = {}
    for isin in isins:
        try:
            # Suche den Ticker über Yahoo Finance
            ticker = yf.Ticker(isin)
            if ticker.info and 'symbol' in ticker.info:
                isin_ticker_map[isin] = ticker.info['symbol']
            else:
                isin_ticker_map[isin] = None  # Kein Ticker gefunden
        except Exception as e:
            print(f"Fehler bei der Verarbeitung von ISIN {isin}: {e}")
            isin_ticker_map[isin] = None
    return isin_ticker_map

print("Starte die Zuordnung von ISINs zu Yahoo Finance-Tickern...")
isin_to_ticker = map_isins_to_yahoo_tickers(unique_isins)

# --- 4. Ergebnisse in eine CSV-Datei schreiben ---
# Erstelle ein DataFrame mit ISIN und Ticker
result_df = pd.DataFrame(list(isin_to_ticker.items()), columns=['ISIN', 'Ticker'])

# Schreibe die Ergebnisse in eine CSV-Datei
result_df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"ISIN zu Ticker-Mapping wurde erfolgreich in {OUTPUT_CSV_PATH} gespeichert.")