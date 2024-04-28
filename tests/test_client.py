import pytest
from omniunibot import OmniUniBotClient, OmniUniBotConfig


def test_client_1():
    client = OmniUniBotClient(bind="tcp://localhost:58655", quiet=False)
    msg_text = f"*Test 1* - _Pass!_"
    client.send(channel_group="test_channels", msg_content={"text": msg_text})


def test_client_2():
    cfg_dict = {
        "server": {
            "bind": "tcp://*:58655",
            "interval": 0.5,
        },
        "client": {
            "bind": "tcp://localhost:58655",
        },
        "log": {
            "level": "DEBUG",
            "dir": "/home/ubuntu/logs/omniunibot",
        },
        "channel_groups": {
            "test_channels": [
                {
                    "platform": "Slack",
                    "webhook": "https://hooks.slack.com/services/xxx/xxx/xxx",
                },
                {
                    "platform": "Lark",
                    "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx-xxxx-xxxx-xxxx-xxx",
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
    client = OmniUniBotClient(config=OmniUniBotConfig.from_dict(cfg_dict), quiet=False)
    msg_text = f"*Test 2* - _Pass!_"
    client.send(channel_group="test_channels", msg_content={"text": msg_text})
    client.send(channel_group="nonexist_channels", msg_content={"text": msg_text})


@pytest.mark.asyncio
async def test_client_3():
    client = OmniUniBotClient(bind="tcp://localhost:58655", quiet=False)
    msg_text = f"*Test 3 (Async)* - _Pass!_"
    await client.send_async(channel_group="test_channels", msg_content={"text": msg_text})
