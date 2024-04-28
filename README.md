# omniunibot

<!-- [![Upload Python Package](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml/badge.svg)](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml) -->

> ⚠️ **For `omniunibot>=0.3.0`, omniunibot will only support `Python>=3.12`.** Please use `omniunibot==0.2.0` for `Python<3.12`.

### 🤖 An omnipotent universal message bot library for python

- Supported platforms
  - Feishu
  - Slack
  - Dingtalk
- Features
  - Non-blocking mode for sending messages
  - Send to multiple platforms with one-line code

### 💻 Installation

- *(via pip)* `pip install -U omniunibot`
- *(via source)* clone this repo && `pip install .`

### 📜 Client-Server Mode

1. Prepare a config file
    - Default config path: `$HOME/configs/omniunibot.json`
    - Config example

        ```json
        {
            "server": {
                "bind": "tcp://*:58655",
                "interval": 0.1
            },
            "client": {
                "bind": "tcp://localhost:58655"
            },
            "log": {
                "level": "DEBUG",
                "dir": "/home/ubuntu/logs/omniunibot"
            },
            "channel_groups": {
                "test_channels": [
                    {
                        "platform": "Slack",
                        "webhook": "https://hooks.slack.com/services/xxxx/xxxx/xxxx"
                    },
                    {
                        "platform": "Lark",
                        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/1a166e72-xxxx-xxxx-xxxx-3ae4f0fb51b7",
                        "secret": "xxx"
                    },
                    {
                        "platform": "DingTalk",
                        "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
                        "secret": "xxx"
                    }
                ]
            }
        }
        ```

2. Start the bot server

    ```sh
    python -m omniunibot.server
    ```

3. Use the client-side code in your code (see examples in [./tests](./tests))

### 📜 Standalone Mode

```py
bot = DingTalkBot(
    "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxx",
    "xxxxxxxxxxxxxx",
    on_success="log",
    on_failure="trace",
)
await bot.send({"text": "`test_dingtalkbot_1` Pass"})

bot = LarkBot(
    "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx-d879-xxxxx-8d7b-xxxxxxxxxx",
    "xxxxxxxxxxxxxxx",
    on_success="log",
    on_failure="trace",
)
await bot.send({"text": "`test_larkbot_1` Pass"})

bot = SlackBot(
    "https://hooks.slack.com/services/xxxxxxxx/xxxxxxxx/xxxxxxxxxx",
    on_success="log",
    on_failure="trace",
)
await bot.send({"text": "`test_slackbot_1` Pass"})
```