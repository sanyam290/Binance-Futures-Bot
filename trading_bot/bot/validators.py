"""
Input validation for trading bot CLI arguments.
All validation errors raise ValueError with a descriptive message.
"""

from typing import Optional, Union

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """
    Validate the trading symbol.

    Rules:
    - Must be a non-empty string
    - Must be uppercase letters only (e.g. BTCUSDT, ETHUSDT)
    - Length between 3 and 20 characters

    Args:
        symbol: The trading pair symbol (e.g. 'BTCUSDT').

    Returns:
        Uppercased symbol string.

    Raises:
        ValueError: If the symbol fails any validation rule.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")

    symbol = symbol.strip().upper()

    if not symbol.isalpha():
        raise ValueError(
            f"Invalid symbol '{symbol}'. Symbol must contain letters only (e.g. BTCUSDT)."
        )

    if not (3 <= len(symbol) <= 20):
        raise ValueError(
            f"Invalid symbol '{symbol}'. Symbol length must be between 3 and 20 characters."
        )

    return symbol


def validate_side(side: str) -> str:
    """
    Validate the order side.

    Args:
        side: Order direction — must be 'BUY' or 'SELL' (case-insensitive).

    Returns:
        Uppercased side string.

    Raises:
        ValueError: If side is not 'BUY' or 'SELL'.
    """
    if not side or not isinstance(side, str):
        raise ValueError("Side must be a non-empty string.")

    side = side.strip().upper()

    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )

    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate the order type.

    Args:
        order_type: Order type — must be 'MARKET' or 'LIMIT' (case-insensitive).

    Returns:
        Uppercased order type string.

    Raises:
        ValueError: If order type is not 'MARKET' or 'LIMIT'.
    """
    if not order_type or not isinstance(order_type, str):
        raise ValueError("Order type must be a non-empty string.")

    order_type = order_type.strip().upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )

    return order_type


def validate_quantity(quantity: Union[str, float]) -> float:
    """
    Validate the order quantity.

    Args:
        quantity: The amount to trade. Must be a positive number.

    Returns:
        Validated quantity as a float.

    Raises:
        ValueError: If quantity is not a positive number.
    """
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid quantity '{quantity}'. Quantity must be a numeric value (e.g. 0.01)."
        )

    if qty <= 0:
        raise ValueError(
            f"Invalid quantity '{qty}'. Quantity must be greater than zero."
        )

    return qty


def validate_price(
    price: Union[str, float, None], order_type: str
) -> Optional[float]:
    """
    Validate the order price.

    For LIMIT orders, price is required and must be a positive number.
    For MARKET orders, price is ignored.

    Args:
        price: The limit price. Required for LIMIT orders.
        order_type: The order type ('MARKET' or 'LIMIT').

    Returns:
        Validated price as float, or None for MARKET orders.

    Raises:
        ValueError: If price is missing for LIMIT order, or is not a positive number.
    """
    if order_type == "MARKET":
        return None

    if price is None or price == "":
        raise ValueError(
            "Price is required for LIMIT orders. Use --price to specify a value."
        )

    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid price '{price}'. Price must be a numeric value (e.g. 30000.50)."
        )

    if p <= 0:
        raise ValueError(
            f"Invalid price '{p}'. Price must be greater than zero."
        )

    return p


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Union[str, float],
    price: Union[str, float, None],
) -> dict:
    """
    Run all validations and return a clean, validated arguments dictionary.

    Args:
        symbol: Trading pair symbol.
        side: Order side (BUY/SELL).
        order_type: Order type (MARKET/LIMIT).
        quantity: Order quantity.
        price: Limit price (required for LIMIT orders).

    Returns:
        Dictionary with validated and normalised values.

    Raises:
        ValueError: On any validation failure.
    """
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_qty = validate_quantity(quantity)
    validated_price = validate_price(price, validated_type)

    return {
        "symbol": validated_symbol,
        "side": validated_side,
        "type": validated_type,
        "quantity": validated_qty,
        "price": validated_price,
    }
