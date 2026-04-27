"""Main entry point for ATLAS-Polymarket trading system."""
from config import get_settings


def main() -> None:
    """Run the trading system."""
    settings = get_settings()
    print(f"ATLAS-Polymarket starting... Paper trade: {settings.paper_trade}")


if __name__ == "__main__":
    main()
