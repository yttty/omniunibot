import base64
import hashlib
import hmac
import time
from typing import Any

import aiohttp

from .base import BaseBot


class LarkBot(BaseBot):
    """
    https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
    """

    _platform = "Lark"

    def __init__(self, webhook: str, secret: str, **kwargs):
        """
        Args:
            webhook (str): webhook from feishu
            secret (str): secret from feishu
        """

        super().__init__(**kwargs)
        self._webhook = webhook
        self._secret = secret
        assert self._secret is not None

    def _sign(self):
        """concat timestamp and secret

        Returns:
            timestamp, sign: _description_
        """
        timestamp = str(round(time.time()))
        string_to_sign = "{}\n{}".format(timestamp, self._secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode("utf-8")
        return timestamp, sign

    async def _is_success_response(self, rsp: dict[str, Any]) -> bool:
        return rsp.get("code", None) == 0

    def _generate_payload(
        self,
        text: str | None = None,
        mention_all: bool = False,
    ):
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
                        "text": ("" if text is None else text) + ("\n" if mention_all else ""),
                    },
                ]
            ]
        }
        if mention_all:
            post_zh_cn["content"][0].append({"tag": "at", "user_id": "all"})
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {"post": {"zh_cn": post_zh_cn}},
        }
        return payload

    async def _send_text(self, text: str, mention_all: bool) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "POST",
                url=self._webhook,
                json=self._generate_payload(text=text, mention_all=mention_all),
            ) as rsp:
                return await rsp.json()
