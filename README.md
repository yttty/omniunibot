# omniunibot

[![Upload Python Package](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml/badge.svg)](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml)

### 🤖 An omnipotent universal message bot library for python
- Supported platforms
    - Dingtalk
    - Feishu
    - WeChat Work (WeCom)
- Features
    - Non-blocking mode for sending messages
    - Send to multiple platforms with one-line code

### 💻 Installation
- *(via pip)* `pip install -U omniunibot`
- *(via source)* clone this repo && `python setup.py install` or `python setup.py develop`

### 📜 Usage

#### Standalone non-blocking mode
1. Prepare a config file
    - Default config path: `$HOME/configs/omniunibot.json`
    - Config example
        ```json
        {
            "channels": {
                "test-channels": [
                    {
                        "platform": "feishu",
                        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx-xxxxx",
                        "secret": "xxxxx"
                    },
                    {
                        "platform": "dingtalk",
                        "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxxxx",
                        "secret": "SECxxxxx"
                    },
                    {
                        "platform": "wecom",
                        "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx-xxxxx"
                    }
                ]
            },
            "bind": "tcp://localhost:58655"
        }
        ```
2. Start the bot server
    ```sh
    python -m omniunibot
    ```

3. Use the client-side code in your code
    ```py
    from omniunibot import OmniUniBotClient

    client = OmniUniBotClient("tcp://*:58655")
    client.send(
        channel="test-channels",
        title="msgTitle",
        msg="msgContent"
    )

    ```

#### Integration mode (Blocking mode, not recommended)

```py
# import bots
from omniunibot import FeishuBot, DingTalkBot, WeComBot

# initialize bots
bot = FeishuBot('<webhook_id>', '<secret>')
bot = DingTalkBot('<token>', '<secret>')
bot = WeComBot('<token>')

# send message
bot.sendQuickMessage('Test Passed')
```

You could check the code example in `./example`
