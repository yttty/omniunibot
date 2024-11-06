import pytest

from omniunibot import OmniUniBotClient, OmniUniBotConfig


def test_client_1():
    client = OmniUniBotClient(bind="tcp://localhost:58655", quiet=False)
    msg_text = f"*Test 1* - _Pass!_"
    client.send(channel_group="test_channels", msg_content={"text": msg_text}, mention_all=False)


@pytest.mark.asyncio
async def test_client_2():
    client = OmniUniBotClient(bind="tcp://localhost:58655", quiet=False)
    msg_text = f"*Test 2 (Async)* - _Pass!_"
    await client.send_async(channel_group="test_channels", msg_content={"text": msg_text}, mention_all=True)
