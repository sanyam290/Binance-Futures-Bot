"""
Binance Futures Testnet client factory.
Reads API credentials from environment variables and returns a configured client.
"""

import os
from dotenv import load_dotenv
from binance.um_futures import UMFutures

from bot.logging_config import setup_logger

load_dotenv()

logger = setup_logger()

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


def get_client() -> UMFutures:
    """
    Create and return an authenticated Binance USD-M Futures Testnet client.

    Reads BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET from the
    environment (or .env file).

    Returns:
        Authenticated UMFutures client pointed at the testnet.

    Raises:
        EnvironmentError: If API key or secret is missing.
        Exception: If the client cannot be initialised.
    """
    api_key = os.getenv("BINANCE_TESTNET_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET", "").strip()

    if not api_key:
        logger.error("Missing environment variable: BINANCE_TESTNET_API_KEY")
        raise EnvironmentError(
            "BINANCE_TESTNET_API_KEY is not set. "
            "Please add it to your .env file."
        )

    if not api_secret:
        logger.error("Missing environment variable: BINANCE_TESTNET_API_SECRET")
        raise EnvironmentError(
            "BINANCE_TESTNET_API_SECRET is not set. "
            "Please add it to your .env file."
        )

    logger.debug("Initialising Binance Futures Testnet client.")

    try:
        client = UMFutures(
            key=api_key,
            secret=api_secret,
            base_url=TESTNET_BASE_URL,
        )
        logger.info("Binance Futures Testnet client initialised successfully.")
        return client
    except Exception as exc:
        logger.exception("Failed to initialise Binance client: %s", exc)
        raise
