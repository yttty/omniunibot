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
from loguru import logger

from .base import BaseBot


class DingTalkBot(BaseBot):
    """
    https://open.dingtalk.com/document/robots/custom-robot-access
    """

    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def _getSignedUrlForDingDing(self):
        baseurl = 'https://oapi.dingtalk.com/robot/send?'
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc,
                             string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        signed_url = baseurl + "&access_token=" + self.token + "&timestamp=" + str(
            timestamp) + "&sign=" + sign
        return signed_url

    def _onErrorResponse(self, response) -> int:
        logger.error(
            f"Code = {response['errcode']}. Message = {response['errmsg']}."
        )
        return response['errcode']

    def _onSuccessResponse(self, response=None) -> int:
        logger.info("Success.")
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
        r = requests.post(self._getSignedUrlForDingDing(), json=payload)
        response = r.json()
        if response['errcode'] == 0:
            self._onSuccessResponse()
        else:
            self._onErrorResponse(response)

    def sendQuickMessage(self, msg: str):
        r = requests.post(self._getSignedUrlForDingDing(),
                          json=self.generatePayload(msg))
        response = r.json()
        if response['errcode'] == 0:
            self._onSuccessResponse()
        else:
            self._onErrorResponse(response)

