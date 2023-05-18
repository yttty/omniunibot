"""
Description : Bots for WXWork
"""

import requests
import traceback
from loguru import logger

from .base import BaseBot


class WeComBot(BaseBot):
    """
    https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(self, webhook: str, **kwargs):
        """
        Args:
            webhook (str): the webhook from wxwork
        """
        self.webhook = webhook

    def _onErrorResponse(self, response) -> int:
        logger.error(
            f"Code = {response['errcode']}. Message = {response['errmsg']}."
        )
        return response['errcode']

    def _onSuccessResponse(self, response=None) -> int:
        logger.debug("Successully sent message to WeCom.")
        return 0

    def generatePayload(self, msgtype: str, **kwargs):
        assert msgtype in ["markdown", "text", "image"], "Unsupported msgtype"
        payload = {"msgtype": msgtype, msgtype: {}}

        if msgtype == "text" or msgtype == "markdown":
            try:
                payload[msgtype]["content"] = kwargs["content"]
                if "mentioned_list" in kwargs:
                    payload[msgtype]["mentioned_list"] = kwargs[[
                        "mentioned_list"
                    ]]
                if "mentioned_mobile_list" in kwargs:
                    payload[msgtype]["mentioned_mobile_list"] = kwargs[[
                        "mentioned_mobile_list"
                    ]]
            except KeyError:
                raise KeyError("Missing msg content")
        elif msgtype == "image":
            try:
                payload[msgtype]["base64"] = kwargs["base64"]
                payload[msgtype]["md5"] = kwargs["md5"]
            except KeyError:
                raise KeyError("Missing image args")

        return payload

    def sendMessage(self, payload: dict):
        logger.debug(f"Get message: {payload}")
        try:
            r = requests.post(self.webhook, json=payload)
            response = r.json()
            if response['errcode'] == 0:
                self._onSuccessResponse()
            else:
                self._onErrorResponse(response)
        except Exception as e:
            logger.error(f"Caught Exception {str(e)}")

    def sendQuickMessage(self, text: str):
        logger.debug(f"Get text Message: {text}")
        try:
            r = requests.post(self.webhook,
                              json=self.generatePayload(msgtype="text",
                                                        content=text))
            response = r.json()
            if response['errcode'] == 0:
                self._onSuccessResponse()
            else:
                self._onErrorResponse(response)
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")

    def sendImage(self, imgPath: str):
        raise NotImplementedError
