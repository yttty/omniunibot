import traceback
from loguru import logger
from typing import Optional, Dict
from slack_sdk.webhook import WebhookClient, webhook_response

from .base import BaseBot


class SlackBot(BaseBot):
    """
    https://slack.dev/python-slack-sdk/
    """

    def __init__(self, webhook: str):
        """
        Args:
            webhook (str): webhook from slack `Incoming Webhooks`
        """

        self.webhook = webhook
        self.slack_client = WebhookClient(self.webhook)

    def _onErrorResponse(self, response: webhook_response) -> int:
        """
        Args:
            response (webhook_response): https://slack.dev/python-slack-sdk/api-docs/slack_sdk/webhook/webhook_response.html

        Returns:
            int: status_code
        """
        logger.error(
            f"Code = {response.status_code}. Message = {response.body}."
        )
        return response.status_code

    def _onSuccessResponse(self, response=None) -> int:
        logger.debug("Successully sent message to Slack.")
        return 0

    def generatePayload(self, text: str) -> Dict:
        payload = {
            'channel': "what-channel",
            'blocks': [
                # {
                #     'type': 'context',
                #             'elements': [
                #                 {
                #                     'type': 'mrkdwn',
                #                     'text': " "
                #                 }
                #             ]
                # },
                {
                    'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': text
                            }
                }
            ],
            "attachments": [
                {
                    'blocks': [
                        {
                            "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": " "
                                    }
                        }
                    ]
                }
            ]
        }
        return payload

    def sendQuickMessage(self, msg: str):
        logger.debug(f"Get text message: {msg}")
        try:
            response = self.slack_client.send_dict(self.generatePayload(msg))
            if response.status_code != 200:
                self._onErrorResponse(response)
            else:
                self._onSuccessResponse()
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
