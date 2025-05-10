import csv
from pathlib import Path
from .model import Transaction, Trade

def _read_csv(path: str | Path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        yield from csv.DictReader(fh)


def _clean(row: dict[str, str]):
    """Turn empty strings into *None* so Optional fields validate cleanly."""
    return {k: (v or None) for k, v in row.items()}


def load_banking_data(path: str | Path):
    items = [Transaction(**_clean(r)) for r in _read_csv(path)]
    return items


def load_trading_data(path: str | Path):
    items = [Trade(**_clean(r)) for r in _read_csv(path)]
    return items