"""Stock K-line data via akshare (sina source for A-shares, eastmoney for HK)."""

import akshare as ak


def _to_sz_sh(symbol: str) -> str:
    """Convert 6-digit code to sz/sh prefixed format for sina APIs."""
    s = symbol.strip()
    if s.startswith(("sz", "sh", "SZ", "SH")):
        return s.lower()
    if s.startswith(("0", "3")):
        return f"sz{s}"
    if s.startswith(("6", "9")):
        return f"sh{s}"
    return f"sz{s}"


def get_stock_data_cn(symbol: str, start_date: str, end_date: str) -> str:
    """Fetch A-share daily K-line via sina source. symbol: '300661'."""
    code = _to_sz_sh(symbol)
    df = ak.stock_zh_a_daily(
        symbol=code,
        start_date=start_date.replace("-", ""),
        end_date=end_date.replace("-", ""),
        adjust="qfq",
    )
    if df.empty:
        return f"No data for {symbol} ({start_date} ~ {end_date})"
    return df.to_string(index=False)


def get_stock_data_hk(symbol: str, start_date: str, end_date: str) -> str:
    """Fetch HK stock daily K-line. symbol: '00700' or '00700.HK'."""
    code = symbol.replace(".HK", "").replace(".hk", "").zfill(5)
    try:
        df = ak.stock_hk_hist(
            symbol=code, period="daily",
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
            adjust="qfq",
        )
    except Exception:
        # fallback to daily
        df = ak.stock_hk_daily(symbol=code, adjust="qfq")
        if not df.empty and "date" in df.columns:
            import pandas as pd
            df["date"] = pd.to_datetime(df["date"])
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if df.empty:
        return f"No data for {symbol} ({start_date} ~ {end_date})"
    return df.to_string(index=False)
