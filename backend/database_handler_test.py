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
    #"CNE100000296": "BYDDF",
    #"US29786A1060": "ETSY", 
    "IE00B6R52259": "ISACEUR"
    # "US64110L1061": "NFLX", 
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
    size_matrix = (daily_agg
                   .reindex(px_index, fill_value=0)
                   .reindex(price_df.columns, axis=1, fill_value=0))

    # keep zeros: 0 means “no order” for vectorbt.from_orders
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
    user_id = "36fd51ee-dadd-45ee-8577-5a6688463abc"

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

    price_data = vbt.YFData.download(symbols, start=start_date).get("Close")
    price_data = price_data.tz_localize(None)
    price_data.index = price_data.index.normalize()

    size_matrix = build_size_matrix(price_data, trades_df)

    # 🔸 init_cash = 0, um keine Bargeldbestände zu berücksichtigen
    pf = vbt.Portfolio.from_orders(
        close=price_data,
        size=size_matrix,
        size_type='amount',
        init_cash=0,
        freq='D'
    )

    risk_scores = compute_risk_scores(pf)
    print(risk_scores)


if __name__ == "__main__":
    main()
