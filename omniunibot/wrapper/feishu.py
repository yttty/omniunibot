import base64
import time
import hashlib
import hmac
import requests
from loguru import logger

from .base import BaseBot


class FeishuBot(BaseBot):
    """
    https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
    """

    def __init__(self, webhook: str, secret: str):
        """
        Args:
            webhook (str): webhook from feishu
            secret (str): sth. like dwTqF7UgZIPJzO0GZjHxxx
        """

        self.webhook = webhook
        self.secret = secret

    def _sign(self):
        """concat timestamp and secret

        Returns:
            timestamp, sign: _description_
        """
        timestamp = str(round(time.time()))
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode(
            "utf-8"), digestmod=hashlib.sha256).digest()

        # b64 encoding
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return timestamp, sign

    def _onErrorResponse(self, response) -> int:
        logger.error(
            f"Code = {response['code']}. Message = {response['msg']}."
        )
        return response['code']

    def _onSuccessResponse(self, response=None) -> int:
        logger.info("Successully sent message to Feishu.")
        return 0

    def generatePayload(self, text: str):
        timestamp, sign = self._sign()
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "text",
            "content": {
                "text": text
            },
        }
        return payload

    def sendQuickMessage(self, msg: str):
        logger.info(f"Get text message: {msg}")
        try:
            r = requests.post(self.webhook,
                              json=self.generatePayload(msg))
            response = r.json()
            if "code" in response.keys():
                self._onErrorResponse(response)
            else:
                self._onSuccessResponse()
        except Exception as e:
            logger.error(f"Caught Exception {str(e)}")
