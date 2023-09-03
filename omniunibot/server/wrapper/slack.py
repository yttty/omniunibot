from loguru import logger
from typing import Optional, Dict, Union
from slack_sdk.webhook import WebhookClient, WebhookResponse
from pathlib import Path

from .base import BaseBot
from ...common.data_type import MsgType


class SlackBot(BaseBot):
    """
    https://slack.dev/python-slack-sdk/
    """

    def __init__(self, webhook: str, **kwargs):
        """
        Args:
            webhook (str): webhook from slack `Incoming Webhooks`
        """

        self.webhook = webhook
        self.slack_client = WebhookClient(self.webhook)

    def _on_success_response(self) -> None:
        logger.debug("Successully sent message to Slack.")

    def _on_error_response(self, response: WebhookResponse) -> None:
        """
        Args:
            response (WebhookResponse): https://slack.dev/python-slack-sdk/api-docs/slack_sdk/webhook/webhook_response.html
        """
        logger.error(f"Code={response.status_code}. ErrMsg={response.body}.")

    def _on_response(self, response: WebhookResponse) -> None:
        if response.status_code != 200:
            self._on_error_response(response)
        else:
            self._on_success_response()

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

    def _send_image(self, msg_id: str, img_path: Union[str, Path], **kwargs):
        raise NotImplementedError

    def _send_text(self, msg_id: str, text: str, **kwargs):
        logger.debug(f"UUID={msg_id}. Receive text message: {text}")
        resp: WebhookResponse = self.slack_client.send_dict(self._generate_payload(msg_type=MsgType.Text, text=text))
        self._on_response(resp)
