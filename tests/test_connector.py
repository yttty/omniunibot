import pytest
import pytest_asyncio
from omniunibot import DingTalkBot, LarkBot, SlackBot


@pytest.mark.asyncio
async def test_dingtalkbot_1():
    bot = DingTalkBot(
        "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxx",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_dingtalkbot_1` Pass"})


@pytest.mark.asyncio
async def test_larkbot_1():
    bot = LarkBot(
        "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx-d879-xxxxx-8d7b-xxxxxxxxxx",
        "xxxxxxxxxxxxxxx",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_larkbot_1` Pass"})


@pytest.mark.asyncio
async def test_slackbot_1():
    bot = SlackBot(
        "https://hooks.slack.com/services/xxxxxxxx/xxxxxxxx/xxxxxxxxxx",
        on_success="log",
        on_failure="trace",
    )
    await bot.send({"text": "`test_slackbot_1` Pass"})
