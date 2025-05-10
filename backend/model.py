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

    
class Portfolio(BaseModel):
    user_id: str = Field(alias="userId")
    asset_names: List[str] = Field(alias="assetNames")
    asset_amounts: List[float] = Field(alias="assetAmounts")
    summary: str = Field(alias="summary")
    risk_summary: str = Field(alias="riskSummary")
    risk_ratio: float = Field(alias="riskRatio")
    total_risk: float = Field(alias="totalRisk")
    total_return: float = Field(alias="totalReturn")
    tradings: str = Field(alias="tradings")
    transactions: str = Field(alias="transactions")


class Person(BaseModel):
    user_id: str = Field(alias="userId")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    friends: List[str] = Field(alias="friends")
    avatar_link: str = Field(alias="avatarLink")
    trader_profile: str = Field(alias="traderProfile")
    latest: str = Field(alias="latest")
    summary: Optional[str] = Field(alias="summary", default=None)
    portfolio: Portfolio = Field(alias="portfolio")
    
    

    