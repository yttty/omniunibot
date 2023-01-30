"""
Description : Bots for WXWork
"""

import requests
from loguru import logger

from .base import BaseBot


class WXWorkBot(BaseBot):
    """
    https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(self, token: str, **kwargs):
        """
        Args:
            token (str): the key from wxwork
        """
        self.key = token

    def _getUrlForWXWork(self):
        baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?'
        return baseurl + "&key=" + self.key

    def _onErrorResponse(self, response) -> int:
        logger.error(
            f"Code = {response['errcode']}. Message = {response['errmsg']}."
        )
        return response['errcode']

    def _onSuccessResponse(self, response=None) -> int:
        logger.info("Success.")
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
        r = requests.post(self._getUrlForWXWork(), json=payload)
        response = r.json()
        if response['errcode'] == 0:
            self._onSuccessResponse()
        else:
            self._onErrorResponse(response)

    def sendQuickMessage(self, text: str):
        r = requests.post(self._getUrlForWXWork(),
                          json=self.generatePayload(msgtype="text",
                                                    content=text))
        response = r.json()
        if response['errcode'] == 0:
            self._onSuccessResponse()
        else:
            self._onErrorResponse(response)

    def sendImage(self, imgPath: str):
        raise NotImplementedError
