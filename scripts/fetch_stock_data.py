#!/usr/bin/env python3
"""Fetch daily K-line (OHLCV) data via akshare.

Usage: python3 fetch_stock_data.py --ticker 300661 --date 2024-05-10 [--lookback 60]
"""
import argparse
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from dataflows.interface import route_to_vendor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--lookback", type=int, default=60)
    args = parser.parse_args()

    start = (datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days=args.lookback)).strftime("%Y-%m-%d")

    print(f"日线数据: {args.ticker} ({start} ~ {args.date})")
    print("=" * 80)
    try:
        print(route_to_vendor("get_stock_data", args.ticker, start, args.date))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
