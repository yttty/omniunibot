# omniunibot

### 🤖 An omnipotent universal message bot library for python

- Supported platforms
  - Feishu
  - Slack
  - Dingtalk
- Features
  - Non-blocking mode for sending messages
  - Send to multiple platforms with one-line code

### 📜 Run via docker (Recommended)

1. Prepare a config file, for example
    ```json
    {
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
        },
        "debug": true
    }
    ```

2. Set environment `export OMNI_CONFIG=<path to the config file>`

3. Use docker to start the bot server
    ```sh
    docker compose up -d --build
    ```

4. Use the client-side code in your code (see examples in `demo_client`)

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

### Release notes

- For `omniunibot (>=0.6.0)`, it is highly recommended to run via docker compose.
- For `omniunibot (>=0.3.0,<0.5.0)`, omniunibot will only support `Python>=3.12`.
- Please use `omniunibot==0.2.0` for `Python<3.12`.
