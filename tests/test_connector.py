import pytest
import pytest_asyncio
import os
from omniunibot import DingTalkBot, LarkBot, SlackBot


@pytest.mark.asyncio
async def test_dingtalkbot_1():
    bot = DingTalkBot(
        "https://oapi.dingtalk.com/robot/send?access_token=3c47250c218329cb5b9947470c03ca0cd165ba3bbe76daf85c46349624bfb016",
        "SEC38a0909b7aef2c97167770627ce2c598acc323a02898057ebcdcb8a4ad803072",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_dingtalkbot_1` Pass"})


@pytest.mark.asyncio
async def test_larkbot_1():
    bot = LarkBot(
        "https://open.feishu.cn/open-apis/bot/v2/hook/4e7d62bc-d879-4d97-8d7b-72f416f71d7c",
        "oipN9z3OGAJAQ0SjBsSV8g",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_larkbot_1` Pass"})


@pytest.mark.asyncio
async def test_slackbot_1():
    bot = SlackBot(
        "https://hooks.slack.com/services/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",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_slackbot_1` Pass"})
