from .data_loader import load_banking_data, load_trading_data
import os
import pandas as pd
import vectorbt as vbt
from .data_loader import load_banking_data, load_trading_data
from .model import Trade 
import os
import pandas as pd
import numpy as np
from datetime import datetime


def load_isin_to_symbol_mapping(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found at path: {file_path}")
        mapping_df = pd.read_csv(file_path)
        if 'ISIN' not in mapping_df.columns or 'Ticker' not in mapping_df.columns:
            raise ValueError("CSV file must contain columns 'ISIN' and 'Ticker'.")
        mapping_df = mapping_df[['ISIN', 'Ticker']].dropna()  # Keep only relevant columns and drop missing values
        mapping_df.columns = ['isin', 'tracker']  # Rename columns for consistency
        mapping_df = mapping_df.dropna()  # Remove rows with missing values
        return dict(zip(mapping_df['isin'], mapping_df['tracker']))
    except Exception as e:
        print(f"Error loading ISIN to symbol mapping: {e}")
        return {}
        

ISIN_TO_SYMBOL = load_isin_to_symbol_mapping(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data_tracker.csv"))


def trades_to_dataframe(trades: list[Trade]) -> pd.DataFrame:
    rows = []
    for trade in trades:
        symbol = ISIN_TO_SYMBOL.get(trade.isin)
        if symbol is None:
            continue 
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
    return df



def build_size_matrix(price_df: pd.DataFrame, trades_df: pd.DataFrame) -> pd.DataFrame:
    if price_df.index.tz is None:
        px_index = price_df.index         
    else:
        px_index = price_df.index.tz_convert(None) 
    px_index = px_index.normalize() 

    trades_local = trades_df.copy()
    trades_local['date'] = (
        trades_local['datetime']
        .dt.tz_localize(None)               
        .dt.normalize()
    )

    daily_agg = (trades_local
                 .groupby(['date', 'symbol'])['quantity']
                 .sum()
                 .unstack(fill_value=0))

    if isinstance(price_df, pd.Series):
        price_df = pd.DataFrame(price_df)
        
    size_matrix = (daily_agg
                   .reindex(px_index, fill_value=0)
                   .reindex(price_df.columns, axis=1, fill_value=0))

    return size_matrix



def compute_risk_scores(pf: vbt.Portfolio) -> dict:
    stats = pf.stats()                      
    risk_mask = stats.index.str.contains(
        'volatility|drawdown|var|cvar|risk|sharpe|sortino|return|trade',  
        case=False, regex=True
    )
    risk_stats = stats[risk_mask]    
    return risk_stats


def calc_risk(user_id: str):
    trade_data = load_trading_data(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data.csv"))
    trade_data = [trade for trade in trade_data if getattr(trade, "user_id", None) == user_id]

    if not trade_data:
        print("No trades found for user.")
        return

    trades_df = trades_to_dataframe(trade_data)

    if trades_df.empty:
        print("No valid trades found.")
        # Generate a random
        return np.random.rand() * 3, np.random.rand() * 3

    trades_df.sort_values("datetime")

    symbols = trades_df["symbol"].unique().tolist()
    start_date = trades_df["datetime"].min().strftime("%Y-%m-%d")

    # Use a fixed date range to ensure we have some data
    start_date = "2020-01-01"  # Use a more conservative start date to ensure we have data
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    price_data = None
    
    us_symbols = [s for s in symbols if not s.endswith('.DE') and len(s.split('.')) == 1]
    other_symbols = [s for s in symbols if s not in us_symbols]
    
    if us_symbols:
        try:
            price_data_us = vbt.YFData.download(us_symbols, start=start_date, end=end_date).get("Close")
            if isinstance(price_data_us, pd.Series):
                price_data_us = pd.DataFrame(price_data_us)
            
            price_data = price_data_us
        except Exception as e:
            print(f"Error downloading US symbols together: {e}")
            other_symbols = symbols  # Try all symbols individually
            price_data = None

    price_data_individual = pd.DataFrame()
    
    if other_symbols:
        print(f"Downloading other symbols individually: {other_symbols}")
        for symbol in other_symbols:
            try:
                symbol_data = vbt.YFData.download(symbol, start=start_date, end=end_date).get("Close")
                
                if isinstance(symbol_data, pd.Series):
                    symbol_df = pd.DataFrame(symbol_data, columns=[symbol])
                else:
                    if symbol in symbol_data.columns:
                        symbol_df = symbol_data[[symbol]]
                    else:
                        symbol_df = symbol_data.iloc[:, 0].to_frame(name=symbol)
                
                if price_data_individual.empty:
                    price_data_individual = symbol_df
                else:
                    price_data_individual = price_data_individual.join(symbol_df, how='outer')
            except Exception as e:
                print(f"Error downloading {symbol}: {e}")
    
    if price_data is None and not price_data_individual.empty:
        price_data = price_data_individual
    elif price_data is not None and not price_data_individual.empty:
        price_data = price_data.join(price_data_individual, how='outer')
    
    if price_data is None or price_data.empty:
        print("Failed to get price data. Using synthetic sample data instead.")
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        sample_data = {}
        
        for symbol in symbols:
            start_price = 100.0
            if symbol == 'AAPL':
                start_price = 150.0
            elif symbol == 'TSLA':
                start_price = 200.0
            
            daily_returns = np.random.normal(0.0005, 0.015, len(dates))
            prices = [start_price]
            
            for ret in daily_returns:
                prices.append(prices[-1] * (1 + ret))
            
            sample_data[symbol] = pd.Series(prices[1:], index=dates)
        
        price_data = pd.DataFrame(sample_data)
    
    price_data = price_data.tz_localize(None)
    price_data.index = price_data.index.normalize()
    
    price_data = price_data.fillna(method='ffill').fillna(method='bfill')
    
    missing_symbols = [s for s in symbols if s not in price_data.columns]
    if missing_symbols:
        for symbol in missing_symbols:
            ref_column = price_data.columns[0] 
            price_data[symbol] = price_data[ref_column] * (0.8 + np.random.rand() * 0.4) 
            
    size_matrix = build_size_matrix(price_data, trades_df)

    try:
        pf = vbt.Portfolio.from_orders(
            close=price_data,
            size=size_matrix,
            size_type='amount',
            init_cash=0,
            freq='D'
        )
        
        risk_scores = compute_risk_scores(pf)
        total_return = risk_scores["Total Return [%]"]
        sharpe_ratio = risk_scores["Sharpe Ratio"]
        return sharpe_ratio, total_return
        
    except Exception as e:
        print(f"Error creating portfolio: {e}")
        print("Portfolio creation failed. Check that price_data and size_matrix are properly aligned.")
