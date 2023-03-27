# import bots
from omniunibot import FeishuBot, DingTalkBot, WeComBot, SlackBot

# initialize bots
bot = FeishuBot('<webhook>', '<secret>')
bot = DingTalkBot('<webhook>', '<secret>')
bot = WeComBot('<webhook>')
bot = SlackBot('<webhook>')

# send message
bot.sendQuickMessage('Test Passed')
