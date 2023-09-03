import pytest
from omniunibot.server.wrapper.dingtalk import DingTalkBot
from omniunibot.common.data_type import MsgType


def test_dingtalkbot_1():
    bot = DingTalkBot(
        webhook="https://oapi.dingtalk.com/robot/send?access_token=9a045513ee68234eed36308d579901edd5a83e9413d9619233280a1ad6f6b5e9",
        secret="SECbba89f6262b8b2823bb05013df307dc850258e695cd202b5519ad011234fe72e",
    )
    bot.send(msg_type=MsgType.Text, msg_content={"text": "`test_dingtalkbot_1` Pass"})


def test_dingtalkbot_2():
    bot = DingTalkBot("xxx", "xxx")
    bot.send(msg_type=MsgType.Image, msg_content=None)
