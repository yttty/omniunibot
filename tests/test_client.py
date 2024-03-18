from omniunibot import OmniUniBotClient, OmniUniBotConfig
import pytest


def test_client_1():
    client = OmniUniBotClient(bind="tcp://localhost:58655", quiet=False)
    msg_text = f"*Test 1* - _Pass!_"
    client.send(channel_group="test_channels", msg_type="Text", text=msg_text)


def test_client_2():
    cfg_dict = {
        "server": {
            "bind": "tcp://*:58655",
            "interval": 5,
        },
        "client": {
            "bind": "tcp://localhost:58655",
        },
        "channel_groups": {
            "test_channels": [
                {
                    "platform": "Slack",
                    "webhook": "https://hooks.slack.com/services/xxxx/xxxx/xxxx",
                },
                {
                    "platform": "Lark",
                    "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/1a166e72-xxxx-xxxx-xxxx-3ae4f0fb51b7",
                    "secret": "xxxxxx",
                },
                {
                    "platform": "DingTalk",
                    "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxxxxx",
                    "secret": "xxxxxx",
                },
            ]
        },
    }
    client = OmniUniBotClient(config=OmniUniBotConfig.from_dict(cfg_dict))
    msg_text = f"*Test 2* - _Pass!_"
    client.send(channel_group="test_channels", msg_type="Text", text=msg_text)
    client.send(channel_group="nonexist_channels", msg_type="Text", text=msg_text)


@pytest.mark.asyncio
async def test_client_3():
    client = OmniUniBotClient(bind="tcp://localhost:58655")
    msg_text = f"*Test 3 (Async)* - _Pass!_"
    await client.send_async(channel_group="test_channels", msg_type="Text", text=msg_text)
