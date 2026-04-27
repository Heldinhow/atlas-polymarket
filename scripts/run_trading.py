"""Main trading loop for ATLAS-Polymarket."""
import asyncio
import os
from datetime import datetime

from src.agents.layer1 import (
    EsportsMacroAgent,
    SportsMacroAgent,
    PolymarketMacroAgent,
    SentimentMacroAgent,
)
from src.agents.layer4 import (
    CIOSynthesisAgent,
    AlphaDiscoveryAgent,
    CROAgent,
    AutonomousExecutionAgent,
)
from src.core.prism import PRISM
from src.core.janus import JANUS
from src.core.soros_engine import SorosEngine
from src.data.polymarket_client import PolymarketClient
from src.execution.paper_trade import PaperTrader
from src.config import get_settings


async def run_trading_cycle():
    """Run one cycle of the trading system."""
    settings = get_settings()
    print(f"[{datetime.now()}] Starting trading cycle...")

    paper_trade = settings.paper_trade
    trader = PaperTrader() if paper_trade else None

    # Initialize agents
    layer1_agents = [
        EsportsMacroAgent(),
        SportsMacroAgent(),
        PolymarketMacroAgent(),
        SentimentMacroAgent(),
    ]

    cio = CIOSynthesisAgent()
    alpha = AlphaDiscoveryAgent()
    cro = CROAgent()
    executor = AutonomousExecutionAgent(paper_trade=paper_trade)

    # Initialize core systems
    prism = PRISM()
    janus = JANUS()
    soros = SorosEngine()

    # Fetch market data - limit to top 20 by volume to keep prompts manageable
    polymarket = PolymarketClient(api_key=settings.polymarket_api_url)
    all_markets = await polymarket.get_markets()
    # Filter to esports/sports markets and limit to top 20
    markets = sorted(all_markets, key=lambda x: x.get("volume24hr", 0), reverse=True)[:20]
    print(f"Fetched {len(markets)} markets (from {len(all_markets)} total)")

    # Layer 1: Macro analysis
    print("Running Layer 1 (Macro) analysis...")
    layer1_results = []
    for agent in layer1_agents:
        # Summarize markets for prompt (full list too big)
        market_summary = [
            {"question": m.get("question", "")[:80], "volume": m.get("volume24hr", 0)}
            for m in markets[:10]  # Only top 10 in prompt
        ]
        result = await agent.analyze({"markets": market_summary})
        layer1_results.append(result)
        print(f"  {agent.name}: {result.get('regime', 'UNKNOWN')}")

    # Detect regime
    regime_context = {
        "volume": sum(m.get("volume", 0) for m in markets),
        "volatility": "medium",
        "sentiment": "neutral",
    }
    regime = prism.detect_regime(regime_context)
    print(f"Detected regime: {regime.value}")

    # Layer 4: Synthesis
    print("Running Layer 4 (Decision) synthesis...")
    synthesis = await cio.synthesize(
        layer1_output=layer1_results[0],
        layer2_output={},  # Placeholder
        layer3_output={},  # Placeholder
    )
    print(f"  CIO Decision: {synthesis.get('action')}")

    # Execute if confident
    if synthesis.get("action") == "BUY" and synthesis.get("confidence", 0) >= 7:
        signal = {
            "action": synthesis["action"],
            "market": markets[0].get("id") if markets else None,
            "confidence": synthesis["confidence"],
        }

        if trader:
            risk_result = await cro.assess_risk({
                "position": signal,
                "portfolio_value": await trader.get_balance(),
            })
            print(f"  Risk assessment: {risk_result.get('risk_score')}")

        execution = await executor.execute(signal)
        print(f"  Execution: {execution.get('status')}")

    await polymarket.close()
    print(f"[{datetime.now()}] Trading cycle complete.")

    if trader:
        print(f"Balance: ${trader.balance:.2f}")
        print(f"Total P&L: ${trader.get_total_pnl():.2f}")


async def main():
    """Main entry point."""
    print("=" * 50)
    print("ATLAS-Polymarket Trading System")
    print("=" * 50)

    while True:
        try:
            await run_trading_cycle()
            await asyncio.sleep(3600)  # Run hourly
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)  # Wait 1 min on error


if __name__ == "__main__":
    asyncio.run(main())
