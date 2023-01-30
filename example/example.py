# import bots
from omniunibot import FeishuBot, DingTalkBot, WXWorkBot

# initialize bots
bot = FeishuBot(webhook_id, secret)
bot = DingTalkBot(token, secret)
bot = WXWorkBot(token)

# send message
bot.sendQuickMessage('Test Passed')
