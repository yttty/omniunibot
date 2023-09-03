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
from typing import Optional, Union
from pathlib import Path
from loguru import logger

from .base import BaseBot
from ...common.data_type import MsgType


class DingTalkBot(BaseBot):
    """
    https://open.dingtalk.com/document/robots/custom-robot-access
    """

    def __init__(self, webhook: str, secret: str, **kwargs):
        self.webhook = webhook
        self.secret = secret
        assert self.secret is not None

    def _get_signed_url(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        signed_url = self.webhook + "&timestamp=" + str(timestamp) + "&sign=" + sign
        return signed_url

    def _on_success_response(self) -> None:
        logger.debug("Successully sent message to DingTalk.")

    def _on_error_response(self, response) -> None:
        logger.error(f"Code={response['errcode']}. ErrMsg={response['errmsg']}.")

    def _on_response(self, resp: dict) -> None:
        if resp["errcode"] == 0:
            self._on_success_response()
        else:
            self._on_error_response(resp)

    def _generate_payload(
        self,
        msg_type: MsgType,
        text: Optional[str] = None,
        atMobiles: Optional[List[str]] = None,
        atAll: bool = False,
    ):
        payload = {
            "msgtype": "text",
            "text": {"content": text},
            "at": {"isAtAll": atAll},
        }
        if atMobiles is not None:
            payload["at"]["atMobiles"] = atMobiles
        return payload

    def _send_image(self, msg_id: str, img_path: Union[str, Path], **kwargs):
        raise NotImplementedError

    def _send_text(self, msg_id: str, text: str, **kwargs):
        logger.debug(f"UUID={msg_id}. Receive text message: {text}")
        resp = requests.post(self._get_signed_url(), json=self._generate_payload(msg_type=MsgType.Text, text=text))
        self._on_response(resp.json())
