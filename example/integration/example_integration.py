# import bots
from omniunibot import FeishuBot, DingTalkBot, WeComBot

# initialize bots
bot = FeishuBot('<webhook>', '<secret>')
bot = DingTalkBot('<webhook>', '<secret>')
bot = WeComBot('<webhook>')

# send message
bot.sendQuickMessage('Test Passed')
