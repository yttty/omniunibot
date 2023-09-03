from omniunibot import OmniUniBotClient, OmniUniBotConfig


def test_client_1():
    client = OmniUniBotClient(bind="tcp://localhost:58655")
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
                    "webhook": "https://hooks.slack.com/services/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",
                },
                {
                    "platform": "Lark",
                    "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/1a166e72-9dae-4989-a9eb-3ae4f0fb51b7",
                    "secret": "eJ3EE0Ghn5Dp0z11O9k9Sg",
                },
                {
                    "platform": "DingTalk",
                    "webhook": "https://oapi.dingtalk.com/robot/send?access_token=9a045513ee68234eed36308d579901edd5a83e9413d9619233280a1ad6f6b5e9",
                    "secret": "SECbba89f6262b8b2823bb05013df307dc850258e695cd202b5519ad011234fe72e",
                },
            ]
        },
    }
    client = OmniUniBotClient(config=OmniUniBotConfig.from_dict(cfg_dict))
    msg_text = f"*Test 2* - _Pass!_"
    client.send(channel_group="test_channels", msg_type="Text", text=msg_text)
    client.send(channel_group="nonexist_channels", msg_type="Text", text=msg_text)
