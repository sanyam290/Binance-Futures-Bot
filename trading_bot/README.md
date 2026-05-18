# Binance Futures Testnet Trading Bot

A clean, modular Python trading bot for placing MARKET and LIMIT orders on the **Binance Futures Testnet**. Built for beginners, with full validation, logging, and a simple command-line interface.

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
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── sample_logs.txt          # Example log output
```

---

## Assumptions

- You are using **Python 3.10+** (uses `X | Y` union type hints).
- You have a **Binance Futures Testnet** account (free, no real money).
- You are running commands from inside the `trading_bot/` directory.
- LIMIT orders use **GTC** (Good Till Cancelled) as the default time-in-force.
- The bot does **not** use leverage settings — it places raw futures orders as-is.
- Symbol validation is format-based (letters only, 3–20 chars). The bot does **not** pre-fetch the exchange's symbol list to keep things simple and fast.

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

> **Never commit your `.env` file to version control.** Add it to `.gitignore`.

---

## Running the Bot

Run all commands from inside the `trading_bot/` directory.

### MARKET Order — Buy

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### MARKET Order — Sell

```bash
python -m bot.cli --symbol ETHUSDT --side SELL --type MARKET --quantity 0.5
```

### LIMIT Order — Buy

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 30000
```

### LIMIT Order — Sell

```bash
python -m bot.cli --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500.50
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
| `--quantity` | Always                | Amount to trade                               | `0.01`          |
| `--price`    | LIMIT orders only     | Limit price per unit                          | `30000.50`      |

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
- API request parameters
- Full API response
- Any errors with detail

---

## Error Handling

| Error Type            | Cause                                               | Bot Response                                      |
|-----------------------|-----------------------------------------------------|---------------------------------------------------|
| `EnvironmentError`    | Missing API key or secret in `.env`                 | Prints config error, exits with code 1            |
| `ValueError`          | Invalid CLI argument                                | Prints validation error and usage, exits with 1   |
| `ClientError` (4xx)   | Bad request (wrong symbol, insufficient balance...) | Logs full error code and message, exits with 1    |
| `ServerError` (5xx)   | Binance server issue                                | Logs server error, exits with 1                   |
| Unexpected `Exception` | Network timeout, connection refused, etc.          | Logs full traceback, exits with 1                 |

---

## Example Terminal Output

```
--- Binance Futures Testnet Trading Bot ---
  Validated: BUY MARKET | BTCUSDT x 0.01

=======================================================
          ORDER PLACED SUCCESSFULLY
=======================================================
  Order ID   : 3279685045
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
  Avg Price  : 43215.60
  Status     : FILLED
  Time       : 1706123456789
=======================================================
```

---

## Dependencies

| Package          | Version  | Purpose                                |
|------------------|----------|----------------------------------------|
| `python-binance` | 1.0.19   | Binance API client (UMFutures class)   |
| `python-dotenv`  | 1.0.1    | Loads `.env` file into environment     |
