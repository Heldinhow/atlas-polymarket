"""Main entry point for ATLAS-Polymarket trading system."""
import asyncio
from scripts.run_trading import main


if __name__ == "__main__":
    asyncio.run(main())
