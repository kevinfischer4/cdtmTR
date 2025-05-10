from data_loader import load_banking_data, load_trading_data
import os
import pandas as pd
import vectorbt as vbt
from data_loader import load_banking_data, load_trading_data
from model import Trade, Risk  # Make sure your models are imported
import os
import pandas as pd
import vectorbt as vbt
from collections import defaultdict
from datetime import datetime
    


# Mock ISIN to symbol mapping (replace with your actual asset data or lookup logic)
ISIN_TO_SYMBOL = {
    "CNE100000296": "BYDDF",
    "US29786A1060": "ETSY", 
    "US64110L1061": "NFLX", 
    # ... add more
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
    return df.sort_values("datetime")


def main():
    trade_data = load_trading_data(os.path.join(os.getcwd(), "backend", "data", "trading_sample_data.csv"))
    trade_data = trade_data[1:4]

    # This looks good, format is 3 x 5 with Symbol, Number, Number, ISIN
    trades_df = trades_to_dataframe(trade_data)

    if trades_df.empty:
        print("No valid trades found.")
        return

    symbols = trades_df["symbol"].unique().tolist()
    start_date = trades_df["datetime"].min().strftime("%Y-%m-%d")

    # Fetch price data, shape is 235 x 3 with number values for each dimension
    price_data = vbt.YFData.download(symbols, start=start_date).get("Close")
    
    # Initialize size array with 0s with shape 235 x 3
    # Each row is a trading day, same as in price_data and each column a symbol
    size_df = pd.DataFrame(0.0, index=price_data.index, columns=symbols)

    for _, row in trades_df.iterrows():
        symbol = row["symbol"]
        dt = row["datetime"]
        idx = price_data.index.get_indexer([dt], method="nearest")[0]
        if idx == -1:
            continue
        date = price_data.index[idx]
        size_df.loc[date, symbol] += row["quantity"]  # Safe and compatible


    # Cumulative size (positions)
    position_df = size_df.cumsum()

    # Create the portfolio
    # Expects a position size time series with "How many units of this asset were held on this day?""
    portfolio = vbt.Portfolio.from_holding(
        close=price_data,
        size=position_df
    )
    
    
    # Risk metrics
    volatility = portfolio.returns().std() * (252 ** 0.5)
    max_dd = portfolio.max_drawdown()
    sharpe = portfolio.sharpe_ratio(freq='1D')

    summary = (
        f"Volatility: {volatility.mean():.2%}, "
        f"Max Drawdown: {max_dd.mean():.2%}, "
        f"Sharpe Ratio: {sharpe.mean():.2f}"
    )
    risk_score = float((sharpe.mean() - max_dd.mean()) / volatility.mean()) if volatility.mean() != 0 else 0.0


    risk = Risk(summary=summary, ratio=risk_score)

    print(risk.json(indent=2))



if __name__ == "__main__":
    main()
