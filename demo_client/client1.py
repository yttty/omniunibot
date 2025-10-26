import asyncio
import logging

import aiohttp


async def tester():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:9999/push",
            json={"channel_group": "test_channels", "msg_text": "A test message."},
        ) as resp:
            if resp.status == 200:
                return True
            else:
                msg = await resp.json()
                logging.error(str(msg))
                return False


asyncio.run(tester())
