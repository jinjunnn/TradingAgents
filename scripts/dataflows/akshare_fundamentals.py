"""Fundamental data via akshare (sina/cninfo sources, avoiding eastmoney)."""

import akshare as ak


def _to_sz_sh(ticker: str) -> str:
    s = ticker.strip()
    if s.startswith(("sz", "sh", "SZ", "SH")):
        return s.lower()
    if s.startswith(("0", "3")):
        return f"sz{s}"
    if s.startswith(("6", "9")):
        return f"sh{s}"
    return f"sz{s}"


def get_fundamentals_cn(ticker: str, curr_date: str = None) -> str:
    """Company profile + key financial indicators."""
    parts = []

    # 巨潮信息网 - 公司概况
    try:
        df = ak.stock_profile_cninfo(symbol=ticker)
        if not df.empty:
            parts.append(f"公司概况:\n{df.to_string(index=False)}")
    except Exception as e:
        parts.append(f"公司概况: {e}")

    # IPO 信息
    try:
        df = ak.stock_ipo_info(stock=ticker)
        if not df.empty:
            parts.append(f"\nIPO 信息:\n{df.to_string(index=False)}")
    except Exception:
        pass

    return "\n\n".join(parts) if parts else f"No fundamentals for {ticker}"


def get_balance_sheet_cn(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """Balance sheet via sina."""
    code = _to_sz_sh(ticker)
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")
        if df.empty:
            return f"No balance sheet for {ticker}"
        return f"资产负债表 ({ticker}, 最近 4 期):\n{df.head(4).to_string(index=False)}"
    except Exception as e:
        return f"Error: {e}"


def get_cashflow_cn(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """Cash flow statement via sina."""
    code = _to_sz_sh(ticker)
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="现金流量表")
        if df.empty:
            return f"No cash flow data for {ticker}"
        return f"现金流量表 ({ticker}, 最近 4 期):\n{df.head(4).to_string(index=False)}"
    except Exception as e:
        return f"Error: {e}"


def get_income_statement_cn(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """Income statement via sina."""
    code = _to_sz_sh(ticker)
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="利润表")
        if df.empty:
            return f"No income statement for {ticker}"
        return f"利润表 ({ticker}, 最近 4 期):\n{df.head(4).to_string(index=False)}"
    except Exception as e:
        return f"Error: {e}"
