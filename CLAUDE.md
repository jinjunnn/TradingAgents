# TradingAgents - Claude Code Plugin

Multi-agent trading analysis. Use `/analyze TICKER DATE` to run.

## Architecture
- 12 Claude agents collaborate: 4 analysts (parallel) → bull/bear debate → trader → 3-way risk debate → portfolio manager
- Rating: BUY / OVERWEIGHT / HOLD / UNDERWEIGHT / SELL

## Structure
- `agents/` — 12 Agent definitions (Markdown)
- `skills/analyze/` — `/analyze` orchestration skill
- `scripts/` — Python data scripts + `dataflows/` data layer (yfinance, Alpha Vantage)
- `data/reports/` — Generated analysis reports
