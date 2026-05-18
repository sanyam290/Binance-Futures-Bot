"""
Order placement logic for Binance Futures Testnet.
Supports MARKET and LIMIT orders for both BUY and SELL sides.
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from bot.logging_config import setup_logger

logger = setup_logger()


def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Place a futures order on the Binance Futures Testnet.

    Args:
        client:     Authenticated Binance Client (testnet=True).
        symbol:     Trading pair (e.g. 'BTCUSDT').
        side:       'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity:   Amount to trade.
        price:      Required for LIMIT orders; ignored for MARKET orders.

    Returns:
        Order response dictionary from the Binance API.

    Raises:
        BinanceAPIException:   On API-level errors (bad symbol, margin, etc.).
        BinanceOrderException: On order-specific errors.
        Exception:             On unexpected errors.
    """
    params: dict = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price must be provided for LIMIT orders.")
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info(
        "Placing %s %s order | Symbol: %s | Quantity: %s%s",
        side,
        order_type,
        symbol,
        quantity,
        f" | Price: {price}" if price is not None else "",
    )
    logger.debug("Order request params: %s", params)

    try:
        response = client.futures_create_order(**params)
        logger.info(
            "Order placed successfully | Order ID: %s | Status: %s",
            response.get("orderId"),
            response.get("status"),
        )
        logger.debug("Full API response: %s", response)
        return response

    except BinanceAPIException as exc:
        logger.error(
            "Binance API error [%s]: %s",
            exc.status_code,
            exc.message,
        )
        raise

    except BinanceOrderException as exc:
        logger.error(
            "Binance order error [%s]: %s",
            exc.status_code,
            exc.message,
        )
        raise

    except Exception as exc:
        logger.exception("Unexpected error while placing order: %s", exc)
        raise


def print_order_summary(response: dict) -> None:
    """
    Print a clear, formatted summary of a completed order to the terminal.

    Args:
        response: The order response dictionary from the Binance API.
    """
    divider = "=" * 55

    print(f"\n{divider}")
    print("          ORDER PLACED SUCCESSFULLY")
    print(divider)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print(f"  Quantity   : {response.get('origQty', 'N/A')}")

    price = response.get("price")
    if price and float(price) > 0:
        print(f"  Price      : {price}")

    avg_price = response.get("avgPrice")
    if avg_price and float(avg_price) > 0:
        print(f"  Avg Price  : {avg_price}")

    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Time       : {response.get('updateTime', 'N/A')}")
    print(f"{divider}\n")
