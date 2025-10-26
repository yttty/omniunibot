import json

import aiohttp


async def send_text(endpoint: str, channel_group: str, msg_text: str) -> tuple[bool, str]:
    """
    Returns:
        tuple[bool, str]: is_successful, error_msg
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://{endpoint}/push",
            json={"channel_group": channel_group, "msg_text": msg_text},
        ) as resp:
            if resp.status == 200:
                return True, ""
            else:
                msg = await resp.json()
                return False, json.dumps(msg)
