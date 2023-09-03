import pytest
from omniunibot.server.wrapper.lark import LarkBot
from omniunibot.common.data_type import MsgType


def test_larkbot_1():
    bot = LarkBot(
        webhook="https://open.feishu.cn/open-apis/bot/v2/hook/1a166e72-9dae-4989-a9eb-3ae4f0fb51b7",
        secret="eJ3EE0Ghn5Dp0z11O9k9Sg",
    )
    bot.send(msg_type=MsgType.Text, msg_content={"text": "`test_larkbot_1` Pass"})


def test_larkbot_2():
    bot = LarkBot("xxx", "xxx")
    bot.send(msg_type=MsgType.Image, msg_content=None)
