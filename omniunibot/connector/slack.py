from pathlib import Path
from typing import Optional, Dict, Any
from slack_sdk.webhook import WebhookResponse
from slack_sdk.webhook.async_client import AsyncWebhookClient

from ..common.data_type import MsgType
from .base import BaseBot


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

    async def _on_response(self, msg_id: str, rsp: WebhookResponse) -> None:
        """_summary_

        Args:
            msg_id (str): _description_
            rsp (WebhookResponse): https://slack.dev/python-slack-sdk/api-docs/slack_sdk/webhook/webhook_response.html
        """
        if rsp.status_code != 200:
            await self._on_error_response(msg_id, {"code": rsp.status_code, "err_msg": rsp.body})
        else:
            await self._on_success_response(msg_id)

    def _generate_payload(self, msg_type: MsgType, text: Optional[str], **kwargs) -> Dict:
        payload = {
            "channel": " ",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text,
                    },
                }
            ],
            "attachments": [
                {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": " ",
                            },
                        }
                    ]
                }
            ],
        }
        return payload

    async def _send_text(self, text: str, **kwargs) -> WebhookResponse:
        rsp = await self._slack_client.send_dict(self._generate_payload(msg_type=MsgType.Text, text=text))
        return rsp
