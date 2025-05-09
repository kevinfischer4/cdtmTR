from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

# --------------
# Banking models
# --------------

class Side(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TxType(str, Enum):
    PAYIN = "PAYIN"
    PAYOUT = "PAYOUT"
    TRADING = "TRADING"
    EARNINGS = "EARNINGS"
    INTEREST = "INTEREST"
    CARD_ORDER = "CARD_ORDER"
    CARD = "CARD"
    OTHER = "OTHER"


class Transaction(BaseModel):
    user_id: str = Field(alias="userId")
    booking_date: date = Field(alias="bookingDate")
    side: Side
    amount: Decimal
    currency: str
    type: TxType
    mcc: Optional[str] = None
    
    
# --------------
# Trading models
# --------------


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradeKind(str, Enum):
    REGULAR = "REGULAR"
    BONUS = "BONUS"
    SAVINGS_PLAN = "SAVINGSPLAN"
    SPARECHANGE = "SPARECHANGE"
    SAVEBACK = "SAVEBACK"


class Trade(BaseModel):
    user_id: str = Field(alias="userId")
    executed_at: datetime = Field(alias="executedAt")
    isin: str = Field(alias="ISIN")
    direction: Direction
    currency: str
    type: TradeKind = Field(alias="type")
    execution_size: Decimal = Field(alias="executionSize")
    execution_price: Decimal = Field(alias="executionPrice")
    execution_fee: Decimal = Field(alias="executionFee")


# --------------
# Asset models
# --------------


class AssetClass(str, Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    BOND = "BOND"
    FUND = "FUND"
    CRYPTO = "CRYPTO"
    OTHER = "OTHER"


class Asset(BaseModel):
    isin: Optional[str] = Field(alias="ISIN", default=None)
    symbol: Optional[str] = None
    name: str
    currency: str
    asset_class: AssetClass
    description: Optional[str] = None


# --------------
# App models
# --------------


class Risk(BaseModel):
    summary: str = Field(alias="summary")
    ratio: float = Field(alias="ratio")
    
    
class Portfolio(BaseModel):
    user_id: str = Field(alias="userId")
    assets: List[Asset] = Field(alias="assets")
    trades: List[Trade] = Field(alias="trades")
    summary: str = Field(alias="summary")
    risk: Risk = Field(alias="risk")


class Person(BaseModel):
    user_id: str = Field(alias="userId")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    friends: List[str] = Field(alias="friends")
    avatar_link: str = Field(alias="avatarLink")
    description: Optional[str] = Field(alias="description", default=None)
    portfolio: Portfolio = Field(alias="portfolio")
    
    

    