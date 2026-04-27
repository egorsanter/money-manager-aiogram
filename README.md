# money-manager-aiogram 💰

## Description
Telegram bot for personal finance tracking 📊

## Prerequisites
- Python 3.12+ 🐍
- PostgreSQL (local or remote) 🐘
- Make (for running the Makefile) ⚙️
- Telegram bot token (obtain via @BotFather) 🤖

## Quick Start 🚀

```bash
git clone https://github.com/egorsanter/money-manager-aiogram.git
cd money-manager-aiogram
cp .env.example .env
```

Fill in `.env` 📝:

```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

Setup and run the bot ▶️:

```bash
make all
```


## Makefile Commands ⚙️:

```bash
make install       # create venv + install dependencies
make install-dev   # install dependencies + dev tools
make migrate       # apply database migrations
make run           # run the bot
make all           # install + migrate + run
```

## Notes

- Do not commit your `.env` file
- Dev dependencies (pytest, etc.) are in `requirements-dev.txt`