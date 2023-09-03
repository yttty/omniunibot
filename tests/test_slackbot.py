import pytest
from omniunibot.server.wrapper.slack import SlackBot
from omniunibot.common.data_type import MsgType


def test_slackbot_1():
    bot = SlackBot("https://hooks.slack.com/services/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")
    bot.send(msg_type=MsgType.Text, msg_content={"text": "`test_slackbot_1` Pass"})


def test_slackbot_2():
    bot = SlackBot("xxx")
    bot.send(msg_type=MsgType.Image, msg_content=None)
