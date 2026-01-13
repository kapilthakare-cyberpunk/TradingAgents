from datetime import datetime
from tradingagents.data.market_data import (
    get_price_data,
    get_fundamentals,
    get_news,
)
from tradingagents.data.indicators import get_technical_indicators

from tradingagents.agents.debate_agents import (
    TechnicalAgent, FundamentalAgent, NewsAgent, RiskAgent
)
from tradingagents.agents.debate_orchestrator import DebateOrchestrator


class TradingAgentsGraph:
    def __init__(self, debug=False, config=None, llm=None):
        self.debug = debug
        self.config = config or {}
        self.llm = llm

    def _build_context(self, symbol):
        try:
            prices = get_price_data(symbol)
            fundamentals = get_fundamentals(symbol)
            news = get_news(symbol)

            latest_price = (
                float(prices["Close"].iloc[-1])
                if not prices.empty else None
            )

            indicators = (
                get_technical_indicators(prices)
                if not prices.empty else {}
            )

            summary = {
                "latest_price": latest_price,
                "market_cap": fundamentals.get("marketCap"),
                "pe_ratio": fundamentals.get("trailingPE"),
                "sector": fundamentals.get("sector"),
                "technical_indicators": indicators,
                "news_headlines": [n.get("title") for n in news[:5]],
            }

            return summary

        except Exception as e:
            return {
                "error": str(e),
                "symbol": symbol
            }

    def propagate(self, symbol, date=None, fast=False):
        date = date or datetime.today().strftime("%Y-%m-%d")

        context = self._build_context(symbol)

        if fast:
            ti = context.get("technical_indicators", {})
            
            # Use safe gets for dictionary access
            rsi = ti.get("rsi", 50)
            trend = ti.get("trend", "neutral")

            if rsi < 40 and trend == "bullish":
                decision = "BUY"
            elif rsi > 65:
                decision = "SELL"
            else:
                decision = "HOLD"

            return context, {
                "decision": decision,
                "confidence": 0.6,
                "reason": "Rule-based fast strategy"
            }

        if self.debug:
            print("[Market Context]", context)

        if self.llm and "error" not in context:
            # Assuming self.llm has an .analyze method based on usage
            decision = self.llm.analyze(symbol, context)
        else:
            decision = {
                "decision": "HOLD",
                "confidence": 0.5,
                "reason": "No LLM connected or data error"
            }

        return context, decision
