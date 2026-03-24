"""News & sentiment data via akshare (sina/cls/ths sources, avoiding eastmoney)."""

import akshare as ak


def get_news_cn(ticker: str, start_date: str = None, end_date: str = None) -> str:
    """Fetch company-specific news. Uses financial report disclosure as proxy."""
    parts = []

    # 巨潮信息网公告
    try:
        df = ak.stock_zh_a_disclosure_report_cninfo(
            symbol=ticker, market="沪深京",
            start_date=(start_date or "20240101").replace("-", ""),
            end_date=(end_date or "20500101").replace("-", ""),
        )
        if not df.empty:
            parts.append(f"公司公告 ({len(df)} 条):\n{df.head(10).to_string(index=False)}")
    except Exception:
        pass

    # 互动易问答
    try:
        df = ak.stock_irm_cninfo(symbol=ticker)
        if not df.empty:
            parts.append(f"\n互动问答 (最近 5 条):\n{df.head(5).to_string(index=False)}")
    except Exception:
        pass

    if not parts:
        return f"No news found for {ticker}"
    return "\n\n".join(parts)


def get_global_news_cn(curr_date: str = None, look_back_days: int = 7, limit: int = 10) -> str:
    """Fetch global financial news via sina."""
    try:
        df = ak.stock_info_global_sina()
        if df.empty:
            return "No global news"

        result = f"全球财经快讯 (最新 {limit} 条):\n\n"
        for _, row in df.head(limit).iterrows():
            time = row.get("时间", "")
            content = row.get("内容", "")
            result += f"[{time}] {content}\n\n"
        return result
    except Exception as e:
        return f"Error: {e}"


def get_hot_rank() -> str:
    """Fetch stock popularity data via ths (同花顺)."""
    try:
        df = ak.stock_info_global_ths()
        if df.empty:
            return "No hot news"
        result = "热门财经资讯 (同花顺):\n\n"
        for _, row in df.head(15).iterrows():
            title = row.get("标题", "")
            time = row.get("发布时间", "")
            content = str(row.get("内容", ""))[:150]
            result += f"[{time}] {title}\n{content}\n\n"
        return result
    except Exception as e:
        return f"Error: {e}"


def get_stock_comments(ticker: str) -> str:
    """Fetch financial news from cls (财联社)."""
    try:
        df = ak.stock_info_global_cls()
        if df.empty:
            return "No data"
        result = "财联社快讯:\n\n"
        for _, row in df.head(10).iterrows():
            title = row.get("标题", "")
            time = row.get("发布时间", "")
            content = str(row.get("内容", ""))[:150]
            result += f"[{time}] {title}\n{content}\n\n"
        return result
    except Exception as e:
        return f"Error: {e}"
