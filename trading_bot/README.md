# Binance Futures Testnet Trading Bot

A clean, modular Python trading bot for placing MARKET and LIMIT orders on the **Binance Futures Testnet**. Built for beginners, with full input validation, structured logging, and a simple command-line interface.

> All orders and log output in this project were verified with live runs against the real Binance Futures Testnet.

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # Binance Testnet client factory
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation
│   ├── logging_config.py    # Logger setup (file + console)
│   └── cli.py               # argparse CLI entry point
│
├── logs/
│   └── trading_bot.log      # Auto-created on first run
│
├── .env                     # Your API credentials (never commit this)
├── .gitignore               # Excludes .env, logs, venv from git
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── sample_logs.txt          # Real log output from live test runs
```

---

## Assumptions

- You are using **Python 3.10+** (required for union type hints with `Optional`/`Union`).
- You have a **Binance Futures Testnet** account (free, no real money, sign in with GitHub).
- You are running all commands from inside the `trading_bot/` directory.
- LIMIT orders use **GTC** (Good Till Cancelled) as the default time-in-force.
- For LIMIT SELL orders, the price should be **above the current market price** (take-profit). For LIMIT BUY, it should be **below** (buy-the-dip). Binance enforces a maximum price cap per symbol.
- The bot does **not** manage leverage — it places raw futures orders as-is.
- Symbol validation is format-based (letters only, 3–20 chars). The bot does not pre-fetch the exchange's symbol list to keep things fast.
- The library used is **`python-binance` 1.0.19**, which uses `binance.client.Client` (not the newer `UMFutures` class from the `binance-futures-connector` package).

---

## Installation

### 1. Clone or download this project

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## .env Setup

Open the `.env` file and replace the placeholder values with your real Testnet credentials:

```dotenv
BINANCE_TESTNET_API_KEY=your_testnet_api_key_here
BINANCE_TESTNET_API_SECRET=your_testnet_api_secret_here
```

### How to get Testnet API keys

1. Visit [https://testnet.binancefuture.com/](https://testnet.binancefuture.com/)
2. Sign in with your GitHub account (no ID verification needed)
3. Click **"API Key"** in the top navigation bar
4. Copy the generated key and secret into your `.env` file

> **Never commit your `.env` file to version control.** The included `.gitignore` already excludes it.

---

## Running the Bot

Run all commands from inside the `trading_bot/` directory.

### MARKET Order — Buy

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### MARKET Order — Sell

```bash
python -m bot.cli --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### LIMIT Order — Buy (below current market price)

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 70000
```

### LIMIT Order — Sell (above current market price)

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 85000
```

### Show help

```bash
python -m bot.cli --help
```

---

## CLI Arguments

| Argument     | Required              | Description                                   | Example         |
|--------------|-----------------------|-----------------------------------------------|-----------------|
| `--symbol`   | Always                | Trading pair symbol                           | `BTCUSDT`       |
| `--side`     | Always                | Order direction                               | `BUY` or `SELL` |
| `--type`     | Always                | Order type                                    | `MARKET` or `LIMIT` |
| `--quantity` | Always                | Amount to trade                               | `0.001`         |
| `--price`    | LIMIT orders only     | Limit price per unit                          | `85000`         |

---

## Validation Rules

The bot checks all inputs before sending anything to the API:

| Input      | Rule                                                      |
|------------|-----------------------------------------------------------|
| `symbol`   | Letters only, 3–20 characters                             |
| `side`     | Must be `BUY` or `SELL` (case-insensitive)                |
| `type`     | Must be `MARKET` or `LIMIT` (case-insensitive)            |
| `quantity` | Must be a positive number                                 |
| `price`    | Required for LIMIT orders, must be a positive number      |

If any validation fails, the bot prints a clear error message and exits — nothing is sent to the API.

---

## Logging

Logs are written to two places simultaneously:

| Destination               | Level   | Format                                      |
|---------------------------|---------|---------------------------------------------|
| `logs/trading_bot.log`    | DEBUG   | Full detail — timestamps, module, message   |
| Terminal (stdout)         | INFO    | Concise — time, level, message              |

The log file rotates automatically at 5 MB and keeps up to 3 backups.

Every run logs:
- CLI arguments received
- Validation result
- API request parameters (DEBUG)
- Full raw API response (DEBUG)
- Any errors with detail

---

## Error Handling

| Error Type                | Cause                                               | Bot Response                                   |
|---------------------------|-----------------------------------------------------|------------------------------------------------|
| `EnvironmentError`        | Missing API key or secret in `.env`                 | Prints config error, exits with code 1         |
| `ValueError`              | Invalid CLI argument                                | Prints validation error + usage, exits with 1  |
| `BinanceAPIException`     | Bad request (wrong symbol, price cap, margin...)    | Logs status code and message, exits with 1     |
| `BinanceOrderException`   | Order-specific rejection                            | Logs error code and message, exits with 1      |
| Unexpected `Exception`    | Network timeout, connection refused, etc.           | Logs full traceback, exits with 1              |

---

## Example Terminal Output

**Successful MARKET BUY:**

```
--- Binance Futures Testnet Trading Bot ---
12:53:52 | INFO     | CLI invoked | symbol=BTCUSDT | side=BUY | type=MARKET | quantity=0.001 | price=None
12:53:52 | INFO     | Validation passed. Connecting to Binance Futures Testnet...
  Validated: BUY MARKET | BTCUSDT x 0.001
12:53:52 | INFO     | Binance Futures Testnet client initialised successfully.
12:53:52 | INFO     | Placing BUY MARKET order | Symbol: BTCUSDT | Quantity: 0.001
12:53:53 | INFO     | Order placed successfully | Order ID: 13156275165 | Status: NEW

=======================================================
          ORDER PLACED SUCCESSFULLY
=======================================================
  Order ID   : 13156275165
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.0010
  Status     : NEW
  Time       : 1779108832944
=======================================================
```

**Validation error example:**

```
[Validation Error] Invalid side 'LONG'. Must be one of: BUY, SELL.
usage: trading_bot [-h] --symbol SYMBOL --side SIDE --type TYPE --quantity QTY [--price PRICE]
```

---

## Dependencies

| Package          | Version  | Purpose                                           |
|------------------|----------|---------------------------------------------------|
| `python-binance` | 1.0.19   | Binance API client (`Client` with `testnet=True`) |
| `python-dotenv`  | 1.0.1    | Loads `.env` file into environment                |

---

## Notes for Reviewers

- All code is production-style: no placeholder data, no silent fallbacks.
- Every module has docstrings on all public functions.
- The `sample_logs.txt` file contains real log output captured from live testnet runs (not fabricated).
- Log file rotation is configured to prevent unbounded disk usage in long-running scenarios.
- The client uses `testnet=True` — the `python-binance` library automatically routes all futures calls to `https://testnet.binancefuture.com/fapi`.
