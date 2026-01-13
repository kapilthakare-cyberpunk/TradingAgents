from colorama import Fore, Style, init
init(autoreset=True)
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.llm.llm_engine import LLMEngine
from tradingagents.backtest.backtester import Backtester
from tradingagents.backtest.metrics import compute_metrics
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 1

config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "alpha_vantage",
    "news_data": "alpha_vantage",
}

# Initialize LLM
llm = LLMEngine(model="gpt-4o-mini")

# Initialize Trading Agent (now supports multi-agent debate internally)
ta = TradingAgentsGraph(debug=True, config=config, llm=llm)

# =============================
# 🔹 LIVE ANALYSIS (Debate Mode)
# =============================
print(f"\n{Fore.LIGHTMAGENTA_EX}=== LIVE ANALYSIS (AI DEBATE) ==={Style.RESET_ALL}")
_, decision = ta.propagate("NVDA", "2024-05-10")
print("\nFinal Decision:\n", decision)

# =============================
# 🔹 BACKTESTING MODE
# =============================
print(f"\n{Fore.LIGHTBLUE_EX}=== BACKTESTING MODE ==={Style.RESET_ALL}")

bt = Backtester(ta, initial_capital=100000)
results = bt.run("NVDA", "2024-01-01", "2024-06-01")

final = results[-1]
print("\nBacktest Result:")
print("Final Capital:", round(final["capital"], 2))
print("Open Position:", final["position"])

# Compute and display performance metrics
metrics = compute_metrics(results, initial_capital=100000)

print("\nPerformance Metrics:")
for k, v in metrics.items():
    print(f"{k}: {v}")


print(f"\n{Fore.LIGHTCYAN_EX}=== PAPER TRADING MODE ==={Style.RESET_ALL}")

paper = PaperTrader(ta, "NVDA", capital=100000)
paper.run(interval=300)  # every 5 minutes