from typing import Any, Dict

from slack_sdk.webhook import WebhookResponse
from slack_sdk.webhook.async_client import AsyncWebhookClient

from .base import BaseBot, MsgType


class SlackBot(BaseBot):
    """
    https://slack.dev/python-slack-sdk/
    """

    _platform = "Slack"

    def __init__(self, webhook: str, slack_webhoot_client_kwargs: Dict[str, Any] = {"timeout": 5}, **kwargs):
        """
        Args:
            webhook (str): webhook from slack `Incoming Webhooks`
            slack_webhoot_client_kwargs: to be passed to slack sdk
        """

        super().__init__(**kwargs)
        self._webhook = webhook
        self._slack_client = AsyncWebhookClient(self._webhook, **slack_webhoot_client_kwargs)

    async def _is_success_response(self, rsp: WebhookResponse | Any) -> bool:
        """_summary_

        Args:
            msg_id (str): _description_
            rsp (WebhookResponse): https://slack.dev/python-slack-sdk/api-docs/slack_sdk/webhook/webhook_response.html
        """

        return getattr(rsp, "status_code", None) == 200

    def _generate_payload(
        self,
        msg_type: MsgType,
        text: str = "",
        markdown: str = "",
        mention_all: bool = False,
    ) -> Dict:
        match msg_type:
            case MsgType.Text:
                return {
                    "text": text + ("\n<!channel>" if mention_all else ""),
                }
            case MsgType.Markdown:
                return {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": markdown + ("\n<!channel>" if mention_all else ""),
                            },
                        },
                    ],
                }
            case _:
                raise NotImplementedError

    async def _send_text(self, text: str, mention_all: bool) -> dict[str, Any]:
        webhook_response = await self._slack_client.send_dict(
            self._generate_payload(msg_type=MsgType.Text, text=text, mention_all=mention_all)
        )
        return {"status_code": webhook_response.status_code, "body": webhook_response.body}

    async def _send_markdown(self, msg_md: str, mention_all: bool) -> dict[str, Any]:
        webhook_response = await self._slack_client.send_dict(
            self._generate_payload(msg_type=MsgType.Markdown, markdown=msg_md, mention_all=mention_all)
        )
        return {"status_code": webhook_response.status_code, "body": webhook_response.body}
