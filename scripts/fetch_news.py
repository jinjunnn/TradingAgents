#!/usr/bin/env python3
"""Fetch news and sentiment data via akshare.

Usage: python3 fetch_news.py --ticker 300661 --date 2024-05-10
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

    # 个股新闻
    print(f"个股新闻: {args.ticker}")
    print("=" * 80)
    try:
        print(route_to_vendor("get_news", args.ticker))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    # 全球财经新闻
    print(f"\n{'=' * 80}")
    print("全球财经新闻")
    print("=" * 80)
    try:
        print(route_to_vendor("get_global_news"))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    # 舆情热度
    print(f"\n{'=' * 80}")
    print("舆情热度排名")
    print("=" * 80)
    try:
        print(route_to_vendor("get_hot_rank"))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    # 个股评论
    print(f"\n{'=' * 80}")
    print(f"个股讨论: {args.ticker}")
    print("=" * 80)
    try:
        print(route_to_vendor("get_stock_comments", args.ticker))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
