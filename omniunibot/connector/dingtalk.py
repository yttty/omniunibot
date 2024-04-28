import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import List
import aiohttp
from pathlib import Path

from ..common.data_type import MsgType
from .base import BaseBot


class DingTalkBot(BaseBot):
    """
    https://open.dingtalk.com/document/robots/custom-robot-access
    """

    _platform = "DingTalk"

    def __init__(self, webhook: str, secret: str, **kwargs):
        super().__init__(**kwargs)
        self._webhook = webhook
        self._secret = secret
        assert self._secret is not None

    def _get_signed_url(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self._secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self._secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        signed_url = self._webhook + "&timestamp=" + str(timestamp) + "&sign=" + sign
        return signed_url

    async def _on_response(self, msg_id: str, rsp: dict) -> None:
        """_summary_

        Args:
            msg_id (str): _description_
            rsp (dict): _description_
        """
        if rsp["errcode"] == 0:
            await self._on_success_response(msg_id)
        else:
            await self._on_error_response(msg_id, rsp)

    def _generate_payload(
        self,
        msg_type: MsgType,
        text: str | None = None,
        atMobiles: List[str] | None = None,
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

    async def _send_text(self, text: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "POST",
                url=self._get_signed_url(),
                json=self._generate_payload(msg_type=MsgType.Text, text=text, **kwargs),
            ) as rsp:
                return await rsp.json()
