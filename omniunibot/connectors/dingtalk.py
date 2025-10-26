import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, List

import aiohttp

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

    async def _is_success_response(self, rsp: dict[str, Any]) -> bool:
        return rsp.get("errcode", None) == 0

    def _generate_payload(
        self,
        text: str | None = None,
        at_mobiles: List[str] = [],
        at_all: bool = False,
    ):
        payload = {
            "msgtype": "text",
            "text": {"content": text},
        }
        if at_all:
            payload["at"] = {"isAtAll": at_all}
        elif at_mobiles:
            payload["at"] = {"atMobiles": at_mobiles}
        return payload

    async def _send_text(self, text: str, mention_all: bool) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "POST",
                url=self._get_signed_url(),
                json=self._generate_payload(text=text, at_all=mention_all),
            ) as rsp:
                return await rsp.json()
