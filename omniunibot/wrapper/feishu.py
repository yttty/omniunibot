import base64
import time
import hashlib
import hmac
import requests
import traceback
from loguru import logger
from typing import List, Optional

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
        logger.debug("Successully sent message to Feishu.")
        return 0

    def generatePayload(self,
                        text: str,
                        title: Optional[str] = None):
        """Generate payload to send, using message type `post`, see the document for details

        Args:
            text (str): _description_
            title (Optional[str], optional): _description_. Defaults to None.
            at_uid (Optional[List[str]], optional): uids to at. Defaults to None.
        """
        timestamp, sign = self._sign()
        post_zh_cn = {
            "content": [
                [
                    {
                        "tag": "text",
                        "text": text
                    }
                ]
            ]
        }
        if title:
            post_zh_cn["title"] = title
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {
                "post": {
                        "zh_cn": post_zh_cn
                }
            }
        }
        return payload

    def sendQuickMessage(self, msg: str):
        logger.debug(f"Get text message: {msg}")
        try:
            r = requests.post(self.webhook,
                              json=self.generatePayload(msg))
            response = r.json()
            if "code" in response.keys() and response['code'] != 0:
                self._onErrorResponse(response)
            else:
                self._onSuccessResponse()
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
