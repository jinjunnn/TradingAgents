#!/usr/bin/env python3
"""Fetch fundamental data via akshare.

Usage: python3 fetch_fundamentals.py --ticker 300661 --date 2024-05-10
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from dataflows.interface import route_to_vendor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()

    sections = [
        ("公司基本面", "get_fundamentals"),
        ("资产负债表", "get_balance_sheet"),
        ("现金流量表", "get_cashflow"),
        ("利润表", "get_income_statement"),
    ]

    for title, method in sections:
        print(f"\n{'=' * 80}")
        print(f"{title}: {args.ticker}")
        print("=" * 80)
        try:
            print(route_to_vendor(method, args.ticker))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
