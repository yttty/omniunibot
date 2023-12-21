# omniunibot

<!-- [![Upload Python Package](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml/badge.svg)](https://github.com/yttty/omniunibot/actions/workflows/python-publish.yml) -->

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

### 📜 Usage

1. Prepare a config file
    - Default config path: `$HOME/configs/omniunibot.json`
    - Config example

        ```json
        {
            "server": {
                "bind": "tcp://*:58655",
                "interval": 0.5
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

3. Use the client-side code in your code
    - Example: [./example/client_example.py](./example/client_example.py)
