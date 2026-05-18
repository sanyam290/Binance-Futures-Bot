"""
Command-line interface for the Binance Futures Testnet Trading Bot.

Usage examples:
  python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  python -m bot.cli --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3000
"""

import argparse
import sys

from bot.client import get_client
from bot.orders import place_order, print_order_summary
from bot.validators import validate_all
from bot.logging_config import setup_logger

logger = setup_logger()


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser for the trading bot CLI.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description=(
            "Binance Futures Testnet Trading Bot\n"
            "Place MARKET or LIMIT orders on the Binance Futures Testnet."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01\n"
            "  python -m bot.cli --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3000\n"
        ),
    )

    parser.add_argument(
        "--symbol",
        required=True,
        metavar="SYMBOL",
        help="Trading pair symbol (e.g. BTCUSDT, ETHUSDT).",
    )
    parser.add_argument(
        "--side",
        required=True,
        metavar="SIDE",
        help="Order side: BUY or SELL.",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        metavar="TYPE",
        help="Order type: MARKET or LIMIT.",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        metavar="QTY",
        help="Quantity to trade (e.g. 0.01).",
    )
    parser.add_argument(
        "--price",
        required=False,
        default=None,
        metavar="PRICE",
        help="Limit price (required for LIMIT orders, e.g. 30000.50).",
    )

    return parser


def main() -> None:
    """
    Entry point for the trading bot CLI.
    Parses arguments, validates inputs, and places the order.
    """
    parser = build_parser()
    args = parser.parse_args()

    print("\n--- Binance Futures Testnet Trading Bot ---")
    logger.info(
        "CLI invoked | symbol=%s | side=%s | type=%s | quantity=%s | price=%s",
        args.symbol,
        args.side,
        args.order_type,
        args.quantity,
        args.price,
    )

    try:
        validated = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"\n[Validation Error] {exc}\n")
        parser.print_usage()
        sys.exit(1)

    logger.info("Validation passed. Connecting to Binance Futures Testnet...")
    print(f"  Validated: {validated['side']} {validated['type']} | {validated['symbol']} x {validated['quantity']}")

    try:
        client = get_client()
    except EnvironmentError as exc:
        logger.error("Client setup failed: %s", exc)
        print(f"\n[Configuration Error] {exc}\n")
        sys.exit(1)
    except Exception as exc:
        logger.exception("Unexpected error during client setup: %s", exc)
        print(f"\n[Error] Failed to initialise client: {exc}\n")
        sys.exit(1)

    try:
        response = place_order(
            client=client,
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"],
        )
        print_order_summary(response)

    except Exception as exc:
        print(f"\n[Order Error] {exc}\n")
        print("Check logs/trading_bot.log for full details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
