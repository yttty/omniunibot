import base64
import time
import hashlib
import hmac
import requests
from loguru import logger
from typing import Optional, Union
from pathlib import Path

from .base import BaseBot
from ...common.data_type import MsgType


class LarkBot(BaseBot):
    """
    https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
    """

    def __init__(self, webhook: str, secret: str, **kwargs):
        """
        Args:
            webhook (str): webhook from feishu
            secret (str): secret from feishu
        """

        self.webhook = webhook
        self.secret = secret
        assert self.secret is not None

    def _sign(self):
        """concat timestamp and secret

        Returns:
            timestamp, sign: _description_
        """
        timestamp = str(round(time.time()))
        string_to_sign = "{}\n{}".format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # b64 encoding
        sign = base64.b64encode(hmac_code).decode("utf-8")
        return timestamp, sign

    def _on_success_response(self) -> None:
        logger.debug("Successully sent message to Lark.")

    def _on_error_response(self, response) -> None:
        logger.error(f"Code={response['code']}. ErrMsg={response['msg']}.")

    def _on_response(self, resp: dict) -> None:
        if "code" in resp.keys() and resp["code"] != 0:
            self._on_error_response(resp)
        else:
            self._on_success_response()

    def _generate_payload(self, msg_type: MsgType, text: Optional[str] = None, title: Optional[str] = None, **kwargs):
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

    def _send_image(self, msg_id: str, img_path: Union[str, Path], **kwargs):
        raise NotImplementedError

    def _send_text(self, msg_id: str, text: str, **kwargs):
        logger.debug(f"UUID={msg_id}. Receive text message: {text}")
        r = requests.post(self.webhook, json=self._generate_payload(msg_type=MsgType.Text, text=text))
        self._on_response(r.json())
