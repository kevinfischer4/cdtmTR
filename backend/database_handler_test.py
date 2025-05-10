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
    

#"User" = "36fd51ee-dadd-45ee-8577-5a6688463abc"

# Mock ISIN to symbol mapping (replace with your actual asset data or lookup logic)
ISIN_TO_SYMBOL = {
    "US06417N1037": "MCP",
  "US070450Y1038": "VJET",
  "DE000SU47L30": "WDI.DE",
  "KYG9828G1082": "09988.HK",
  "DE000WACK012": "WAC.DE",
  "US0921131092": "ADBE",
  "MHY1771G1026": "MHY.TO",
  "US98980F1049": "XELA",
  "US29414B1044": "RPM",
  "US98980L1017": "XTNT",
  "IL0011595993": "NICE",
  "IL0011582033": "TEVA",
  "SE0000163628": "ERIC-B.ST",
  "US57060D1081": "MS.LSE",
  "US5500211090": "ACGL",
  "US9224751084": "SONY",
  "LU0974299876": "AMS.PA",
  "US45784P1012": "ORCL",
  "US98138H1014": "ZEN"

}


def trades_to_dataframe(trades: list[Trade]) -> pd.DataFrame:
    rows = []
    for trade in trades:
        symbol = ISIN_TO_SYMBOL.get(trade.isin)
        if symbol is None:
            continue  # skip unknown assets
        # Localize to UTC
        dt = pd.to_datetime(trade.executed_at)
        if dt.tzinfo is None:
            dt = dt.tz_localize('UTC')
        rows.append({
            'datetime': dt,
            'symbol': symbol,
            'quantity': float(trade.execution_size) if trade.direction == "BUY" else -float(trade.execution_size),
            'price': float(trade.execution_price),
            'isin': trade.isin
        })
    df = pd.DataFrame(rows)
    print(df)
    return df.sort_values("datetime")

# ------------ helper ---------------------------------------------------------

def build_size_matrix(price_df: pd.DataFrame,
                      trades_df: pd.DataFrame) -> pd.DataFrame:
    """Return matrix aligned 1‑for‑1 with price_df.index (daily)."""

    # ---- 1 · normalise the price index ------------------------------------
    if price_df.index.tz is None:
        px_index = price_df.index              # already tz‑naïve
    else:
        px_index = price_df.index.tz_convert(None)   # drop tz info
    px_index = px_index.normalize()            # force HH:MM:SS → 00:00:00

    # ---- 2 · aggregate trades on the same footing -------------------------
    trades_local = trades_df.copy()
    trades_local['date'] = (
        trades_local['datetime']
        .dt.tz_localize(None)                  # safe – no 'errors' kw‑arg
        .dt.normalize()
    )

    daily_agg = (trades_local
                 .groupby(['date', 'symbol'])['quantity']
                 .sum()
                 .unstack(fill_value=0))

    # ---- 3 · align rows & columns -----------------------------------------
    # Check if price_df is a Series and convert to DataFrame if needed
    if isinstance(price_df, pd.Series):
        price_df = pd.DataFrame(price_df)
        
    size_matrix = (daily_agg
                   .reindex(px_index, fill_value=0)
                   .reindex(price_df.columns, axis=1, fill_value=0))

    # keep zeros: 0 means "no order" for vectorbt.from_orders
    return size_matrix



def compute_risk_scores(pf: vbt.Portfolio) -> dict:
    """Liefert Risk‑Kennzahlen, egal wie die Labels in pf.stats() heißen."""
    stats = pf.stats()                      # Series (ein Portfoliokol)
    # pick the rows whose label contains one of these substrings
    risk_mask = stats.index.str.contains(
        'volatility|drawdown|var|cvar|risk|sharpe|sortino|return|trade',   # add/remove terms
        case=False, regex=True
    )

    risk_stats = stats[risk_mask]        # still a Series
    print(risk_stats.to_string())


def main():
    user_id = "01c56b98-55fa-4d8a-ae53-e55192fc9718"

    # Lade alle Trades
    trade_data = load_trading_data(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data.csv"))

    # 🔸 Filter auf Benutzer
    trade_data = [trade for trade in trade_data if getattr(trade, "user_id", None) == user_id]

    if not trade_data:
        print("Keine Trades für diesen Benutzer gefunden.")
        return

    trades_df = trades_to_dataframe(trade_data)

    if trades_df.empty:
        print("Keine gültigen Trades gefunden.")
        return

    symbols = trades_df["symbol"].unique().tolist()
    start_date = trades_df["datetime"].min().strftime("%Y-%m-%d")
    
    print(f"Downloading price data for symbols: {symbols} from {start_date}")
    
    # Use a fixed date range to ensure we have some data
    start_date = "2020-01-01"  # Use a more conservative start date to ensure we have data
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Try direct download for US stocks and fallback to individual download
    price_data = None
    
    # Filter symbols by common US stocks that should work directly
    us_symbols = [s for s in symbols if not s.endswith('.DE') and len(s.split('.')) == 1]
    other_symbols = [s for s in symbols if s not in us_symbols]
    
    if us_symbols:
        try:
            # Try to download US symbols first (these usually work together)
            print(f"Trying direct download for US symbols: {us_symbols}")
            price_data_us = vbt.YFData.download(us_symbols, start=start_date, end=end_date).get("Close")
            if isinstance(price_data_us, pd.Series):
                price_data_us = pd.DataFrame(price_data_us)
            
            print(f"Successfully downloaded US symbols data shape: {price_data_us.shape}")
            price_data = price_data_us
        except Exception as e:
            print(f"Error downloading US symbols together: {e}")
            other_symbols = symbols  # Try all symbols individually
            price_data = None
    
    # Download each non-US symbol individually
    price_data_individual = pd.DataFrame()
    
    if other_symbols:
        print(f"Downloading other symbols individually: {other_symbols}")
        for symbol in other_symbols:
            try:
                symbol_data = vbt.YFData.download(symbol, start=start_date, end=end_date).get("Close")
                print(f"Downloaded {symbol} data type: {type(symbol_data)}")
                
                if isinstance(symbol_data, pd.Series):
                    symbol_df = pd.DataFrame(symbol_data, columns=[symbol])
                else:
                    # If it's already a DataFrame but might have different column names
                    if symbol in symbol_data.columns:
                        symbol_df = symbol_data[[symbol]]
                    else:
                        # Just take the first column and rename it
                        symbol_df = symbol_data.iloc[:, 0].to_frame(name=symbol)
                
                if price_data_individual.empty:
                    price_data_individual = symbol_df
                else:
                    price_data_individual = price_data_individual.join(symbol_df, how='outer')
                
                print(f"Current combined data shape: {price_data_individual.shape}")
            except Exception as e:
                print(f"Error downloading {symbol}: {e}")
    
    # Combine all data frames
    if price_data is None and not price_data_individual.empty:
        price_data = price_data_individual
    elif price_data is not None and not price_data_individual.empty:
        price_data = price_data.join(price_data_individual, how='outer')
    
    # If we still didn't get any data, fallback to using sample data
    if price_data is None or price_data.empty:
        print("Failed to get price data. Using synthetic sample data instead.")
        # Create sample price data with small random movements
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        sample_data = {}
        
        for symbol in symbols:
            # Start with a reasonable price and add small random movements
            start_price = 100.0
            if symbol == 'AAPL':
                start_price = 150.0
            elif symbol == 'TSLA':
                start_price = 200.0
            
            np.random.seed(42)  # For reproducibility
            daily_returns = np.random.normal(0.0005, 0.015, len(dates))
            prices = [start_price]
            
            for ret in daily_returns:
                prices.append(prices[-1] * (1 + ret))
            
            sample_data[symbol] = pd.Series(prices[1:], index=dates)
        
        price_data = pd.DataFrame(sample_data)
    
    # Ensure price_data is properly formatted
    price_data = price_data.tz_localize(None)
    price_data.index = price_data.index.normalize()
    
    # Fill missing values with forward fill and then backward fill
    price_data = price_data.fillna(method='ffill').fillna(method='bfill')
    
    # Print price data preview to check structure
    print("Price data structure:")
    print(price_data.head())
    print(f"Price data shape: {price_data.shape}")
    
    # Ensure all required symbols are present in price_data
    missing_symbols = [s for s in symbols if s not in price_data.columns]
    if missing_symbols:
        print(f"Warning: Missing price data for symbols: {missing_symbols}")
        # Add synthetic data for missing symbols
        for symbol in missing_symbols:
            # Use a similar symbol's data or create synthetic data
            ref_column = price_data.columns[0]  # Use first available column as reference
            price_data[symbol] = price_data[ref_column] * (0.8 + np.random.rand() * 0.4)  # Random scaling
    
    # Build size matrix with available price data
    size_matrix = build_size_matrix(price_data, trades_df)
    
    print("Size matrix structure:")
    print(size_matrix.head())
    print(f"Size matrix shape: {size_matrix.shape}")
    
    # 🔸 init_cash = 0, um keine Bargeldbestände zu berücksichtigen
    try:
        pf = vbt.Portfolio.from_orders(
            close=price_data,
            size=size_matrix,
            size_type='amount',
            init_cash=0,
            freq='D'
        )
        
        risk_scores = compute_risk_scores(pf)
        print(risk_scores)
        
        
        #positions = pf.positions.records_readable
        # Filtere die offenen Positionen (Exit Timestamp ist NaN)
        #open_positions = positions[positions['Exit Timestamp'].isna()]

        # Ausgabe der offenen Positionen mit Symbol und Stückzahl
        #print("Aktuelle offene Positionen im Portfolio:")
        #for _, pos in open_positions.iterrows():
        #    print(
        #        f"Asset: {pos['Column']}, "
        #        f"Stückzahl: {pos['Size']}, "  
        #    )  
        
    except Exception as e:
        print(f"Error creating portfolio: {e}")
        print("Portfolio creation failed. Check that price_data and size_matrix are properly aligned.")


if __name__ == "__main__":
    main()
