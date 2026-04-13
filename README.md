# money-manager-aiogram

## Description
Telegram bot for personal finance tracking.

## Tech stack
- Python 3.12.10  
- aiogram 3.26.0

## Prerequisites
- Python 3.12.10  
- Make (for running the Makefile)  
- Telegram bot token (obtain via @BotFather)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/egorsanter/money-manager-aiogram.git
cd money-manager-aiogram
```

### 2. Create a `.env` file in the root directory with your token:
```bash
BOT_TOKEN=123456:ABCDEF_your_token_here
```

### 3. Run the bot
```bash
make all
```

> This will:
> - Create a Python virtual environment `.venv`
> - Install dependencies from `requirements.txt`
> - Launch the bot