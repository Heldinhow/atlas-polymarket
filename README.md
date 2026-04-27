# ATLAS-Polymarket

Autonomous AI trading framework for Polymarket esports/sports markets, adapted from [ATLAS by General Intelligence Capital](https://github.com/chrisworsey55/atlas-gic).

## Architecture

4-layer hierarchical agent system:

- **Layer 1 (Macro)**: EsportsMacro, SportsMacro, PolymarketMacro, SentimentMacro
- **Layer 2 (Sector)**: EarningsDesk, MetaDesk, ScheduleDesk, OddsDesk
- **Layer 3 (Superinvestor)**: Druckenmiller, Aschenbrenner, Ackman, Baker
- **Layer 4 (Decision)**: CIOSynthesis, AlphaDiscovery, CRO, AutonomousExecution

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Running

```bash
# Paper trade (default)
PAPER_TRADE=true python -m src.main

# Live trade (BE CAREFUL)
PAPER_TRADE=false python -m src.main
```

## Core Systems

- **Autoresearch**: Self-improving agent prompts via git versioning
- **PRISM**: Market regime detection (Bull, Crisis, Rate Tightening, Recovery, Euphoria)
- **JANUS**: Meta-weighting of agent cohorts by accuracy
- **Soros Reflexivity Engine**: Market feedback loop modeling

## Tech Stack

- Python 3.11+
- MiniMax API (LLM)
- PostgreSQL + Redis (storage)
- Polymarket CLOB API