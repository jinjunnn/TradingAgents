---
name: analyze
description: |
  Multi-agent trading analysis system. Run a comprehensive stock analysis with parallel analysts,
  bull/bear investment debate, trading decision, risk debate, and portfolio manager final rating.
  Use when user says "analyze NVDA", "trading analysis for AAPL", or provides a ticker to analyze.
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, Agent
---

# Multi-Agent Trading Analysis

Parse the arguments: `$ARGUMENTS` should contain a TICKER (required) and optionally a DATE (YYYY-MM-DD format). If no date is provided, use today's date.

Example: `/analyze NVDA 2024-05-10` or `/analyze AAPL`

The instrument to analyze is the TICKER from above. Use this exact ticker in every agent invocation, preserving any exchange suffix (e.g. `.TO`, `.L`, `.HK`).

## Phase 1: Parallel Data Analysis

Launch all 4 analyst agents **simultaneously in a single message** (use multiple Agent tool calls in parallel). Pass each agent the ticker and date.

For each agent, the prompt should be:
> Analyze **{TICKER}** as of **{DATE}**. The instrument to analyze is `{TICKER}` — use this exact ticker in every tool call and report.

The 4 agents to launch:
1. **market-analyst** — technical analysis (price data + indicators)
2. **social-analyst** — social media sentiment and company news
3. **news-analyst** — macro news, global events, insider transactions
4. **fundamentals-analyst** — financial statements and company health

Collect their 4 reports. Save each report to `${CLAUDE_PLUGIN_ROOT}/data/reports/{TICKER}_{DATE}_{analyst_name}.md`.

## Phase 2: Investment Debate

Using the 4 reports collected above, run the bull/bear debate:

**Round 1 (and subsequent rounds if depth warrants it):**

1. Launch **bull-researcher** agent with prompt:
   > Here are the analyst reports for {TICKER} as of {DATE}:
   >
   > ## Market Report
   > {market_report}
   >
   > ## Sentiment Report
   > {sentiment_report}
   >
   > ## News Report
   > {news_report}
   >
   > ## Fundamentals Report
   > {fundamentals_report}
   >
   > Build your bullish case for investing in {TICKER}.

2. Launch **bear-researcher** agent with prompt:
   > Here are the analyst reports for {TICKER} as of {DATE}:
   >
   > {same 4 reports}
   >
   > Here is the bull analyst's argument:
   > {bull_argument}
   >
   > Build your bearish case against investing in {TICKER}. Counter the bull's arguments.

3. Launch **research-manager** agent with prompt:
   > Here is the complete investment debate for {TICKER}:
   >
   > ## Analyst Reports
   > {summaries of 4 reports}
   >
   > ## Debate History
   > {bull_argument}
   > {bear_argument}
   >
   > Judge this debate and produce a decisive investment plan for the trader.

Collect the investment plan.

## Phase 3: Trading Decision

Launch **trader** agent with prompt:
> Based on the research team's analysis of {TICKER} as of {DATE}:
>
> ## Investment Plan (from Research Manager)
> {investment_plan}
>
> ## Supporting Analyst Reports
> Market: {brief_market_summary}
> Sentiment: {brief_sentiment_summary}
> News: {brief_news_summary}
> Fundamentals: {brief_fundamentals_summary}
>
> Make your trading decision. End with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**

Collect the trader's decision.

## Phase 4: Risk Debate

Run the 3-way risk debate:

1. Launch **aggressive-risk** agent with prompt:
   > Trader's decision for {TICKER}: {trader_decision}
   >
   > Analyst reports: {4 report summaries}
   >
   > Present the aggressive high-reward perspective.

2. Launch **conservative-risk** agent with prompt:
   > Trader's decision for {TICKER}: {trader_decision}
   >
   > Analyst reports: {4 report summaries}
   >
   > Aggressive analyst's argument: {aggressive_argument}
   >
   > Present the conservative risk-protection perspective. Counter the aggressive view.

3. Launch **neutral-risk** agent with prompt:
   > Trader's decision for {TICKER}: {trader_decision}
   >
   > Analyst reports: {4 report summaries}
   >
   > Aggressive argument: {aggressive_argument}
   > Conservative argument: {conservative_argument}
   >
   > Present a balanced perspective. Challenge both the aggressive and conservative views.

4. Launch **portfolio-manager** agent with prompt:
   > Final decision needed for {TICKER} as of {DATE}.
   >
   > ## Trader's Proposed Plan
   > {trader_decision}
   >
   > ## Risk Debate History
   > Aggressive: {aggressive_argument}
   > Conservative: {conservative_argument}
   > Neutral: {neutral_argument}
   >
   > ## Analyst Reports (reference)
   > {4 report summaries}
   >
   > Deliver your final rating (Buy/Overweight/Hold/Underweight/Sell) and executive summary.

## Phase 5: Final Output

Present the complete analysis result to the user in this format:

---

# Trading Analysis: {TICKER} — {DATE}

## Final Rating: {RATING}

{Portfolio Manager's executive summary}

## Investment Thesis
{Portfolio Manager's detailed thesis}

## Analyst Reports Summary
| Analyst | Key Finding | Signal |
|---------|-------------|--------|
| Technical | {one-line} | Bullish/Neutral/Bearish |
| Sentiment | {one-line} | Bullish/Neutral/Bearish |
| News | {one-line} | Bullish/Neutral/Bearish |
| Fundamentals | {one-line} | Bullish/Neutral/Bearish |

## Debate Summary
**Bull Case**: {one-line summary}
**Bear Case**: {one-line summary}
**Research Manager**: {recommendation}

## Risk Assessment
**Aggressive View**: {one-line}
**Conservative View**: {one-line}
**Neutral View**: {one-line}

---

Save the final report to `${CLAUDE_PLUGIN_ROOT}/data/reports/{TICKER}_{DATE}_final.md`.
