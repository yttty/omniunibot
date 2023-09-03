import pytest
from omniunibot.common.data_type import OmniUniBotChannelConfig, OmniUniBotConfig


def test_channel_config_1():
    cfg_dict = {"platform": "Slack", "webhook": "http://xx.xx.xxx"}
    cfg = OmniUniBotChannelConfig.from_dict(cfg_dict)
    assert cfg == OmniUniBotChannelConfig.from_dict(cfg_dict)
    assert cfg.to_dict() == cfg_dict


def test_channel_config_2():
    cfg_dict = {"platform": "Slack", "webhook": "http://xx.xx.xxx"}
    with pytest.raises(TypeError):
        OmniUniBotChannelConfig.from_dict(cfg_dict) == 0


def test_config_1():
    cfg_dict = {
        "server": {
            "bind": "tcp://*:58655",
            "interval": 0.5,
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
    cfg = OmniUniBotConfig.from_dict(cfg_dict)
    assert cfg == OmniUniBotConfig.from_dict(cfg_dict)
    assert cfg.to_dict() == cfg_dict
