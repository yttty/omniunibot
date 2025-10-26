import asyncio

from omniunibot import send_text

asyncio.run(send_text("localhost:9999", "test_channels", "Another test message!"))
