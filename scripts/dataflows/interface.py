"""Data interface: all data via akshare."""

from .akshare_stock import get_stock_data_cn, get_stock_data_hk
from .akshare_fundamentals import (
    get_fundamentals_cn, get_balance_sheet_cn,
    get_cashflow_cn, get_income_statement_cn,
)
from .akshare_news import get_news_cn, get_global_news_cn, get_hot_rank, get_stock_comments


def detect_market(ticker: str) -> str:
    clean = ticker.strip()
    if clean.upper().endswith(".HK"):
        return "hk"
    if clean.isdigit() and len(clean) == 6:
        return "cn"
    return "us"


METHODS = {
    "get_stock_data": get_stock_data_cn,
    "get_fundamentals": get_fundamentals_cn,
    "get_balance_sheet": get_balance_sheet_cn,
    "get_cashflow": get_cashflow_cn,
    "get_income_statement": get_income_statement_cn,
    "get_news": get_news_cn,
    "get_global_news": get_global_news_cn,
    "get_hot_rank": get_hot_rank,
    "get_stock_comments": get_stock_comments,
}

HK_OVERRIDES = {
    "get_stock_data": get_stock_data_hk,
}


def route_to_vendor(method: str, *args, **kwargs):
    ticker = args[0] if args else kwargs.get("ticker", kwargs.get("symbol", ""))
    market = detect_market(str(ticker))

    if market == "hk" and method in HK_OVERRIDES:
        return HK_OVERRIDES[method](*args, **kwargs)

    if method not in METHODS:
        raise ValueError(f"Method '{method}' not supported")

    return METHODS[method](*args, **kwargs)
