# omniunibot

### An omnipotent universal bot for python
* An omnipotent universal message bot library

### Installation
- *(via pip)* `pip install -U omniunibot`
- *(via source)* clone this repo && `python setup.py install` or `python setup.py develop`

### How to use
```py
# import unibot
from omniunibot import FeishuBot, DingTalkBot, WXWorkBot

# initialize unibot
bot = FeishuBot(webhook_id, secret)
bot = DingTalkBot(token, secret)
bot = WXWorkBot(token)

# send message
bot.sendQuickMessage('Test Passed')
```

You could check the code example in `./example`
