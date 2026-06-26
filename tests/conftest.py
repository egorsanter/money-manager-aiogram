import os

os.environ.setdefault('BOT_TOKEN', '123456:TEST_TOKEN_FOR_TESTS')
os.environ.setdefault(
    'DATABASE_URL',
    'postgresql+asyncpg://test:test@localhost:5432/test',
)