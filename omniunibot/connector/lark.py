import base64
import hashlib
import hmac
import time
from pathlib import Path

import aiohttp

from ..common.data_type import MsgType
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
        # b64 encoding
        sign = base64.b64encode(hmac_code).decode("utf-8")
        return timestamp, sign

    async def _on_response(self, msg_id: str, rsp: dict | None) -> None:
        """_summary_

        Args:
            msg_id (str): _description_
            rsp (dict): _description_
        """
        if rsp.get("code", None) != 0:
            await self._on_error_response(msg_id, rsp)
        else:
            await self._on_success_response(msg_id)

    def _generate_payload(self, msg_type: MsgType, text: str | None = None, title: str | None = None, **kwargs):
        """Generate payload to send, using message type `post`, see the document for details

        Args:
            text (str): _description_
            title (Optional[str], optional): _description_. Defaults to None.
            at_uid (Optional[List[str]], optional): uids to at. Defaults to None.
        """
        timestamp, sign = self._sign()
        post_zh_cn = {"content": [[{"tag": "text", "text": text}]]}
        if title is not None:
            post_zh_cn["title"] = title
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {"post": {"zh_cn": post_zh_cn}},
        }
        return payload

    async def _send_text(self, text: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "POST", url=self._webhook, json=self._generate_payload(msg_type=MsgType.Text, text=text, **kwargs)
            ) as rsp:
                return await rsp.json()
