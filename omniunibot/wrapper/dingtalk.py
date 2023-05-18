"""
Description : Bots for DingDing
"""

import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import List, Optional
import requests
import traceback
from loguru import logger

from .base import BaseBot


class DingTalkBot(BaseBot):
    """
    https://open.dingtalk.com/document/robots/custom-robot-access
    """

    def __init__(self, webhook, secret):
        self.webhook = webhook
        self.secret = secret

    def _getSignedUrlForDingDing(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc,
                             string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        signed_url = self.webhook + "&timestamp=" + str(
            timestamp) + "&sign=" + sign
        return signed_url

    def _onErrorResponse(self, response) -> int:
        logger.error(
            f"Code = {response['errcode']}. Message = {response['errmsg']}."
        )
        return response['errcode']

    def _onSuccessResponse(self, response=None) -> int:
        logger.debug("Successully sent message to DingTalk.")
        return 0

    def generatePayload(self,
                        text: str,
                        atMobiles: Optional[List[str]] = None,
                        atAll: bool = False):
        payload = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "isAtAll": atAll
            }
        }
        if atMobiles is not None:
            payload['at']['atMobiles'] = atMobiles
        return payload

    def sendMessage(self, payload: dict):
        logger.debug(f"Get message: {payload}")
        try:
            r = requests.post(self._getSignedUrlForDingDing(),
                              json=payload)
            response = r.json()
            if response['errcode'] == 0:
                self._onSuccessResponse()
            else:
                self._onErrorResponse(response)
        except Exception as e:
            logger.error(f"Caught Exception {str(e)}")

    def sendQuickMessage(self, msg: str):
        logger.debug(f"Get text message: {msg}")
        try:
            r = requests.post(self._getSignedUrlForDingDing(),
                              json=self.generatePayload(msg))
            response = r.json()
            if response['errcode'] == 0:
                self._onSuccessResponse()
            else:
                self._onErrorResponse(response)
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
