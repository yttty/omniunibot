import zmq
import json
from loguru import logger
from zmq.asyncio import Context
from time import sleep
from typing import Optional


class OmniUniBotClient:
    def __init__(self,
                 bind: str) -> None:
        """Initialize OmniUniBot Client

        Args:
            bind (str): the bind addr
        """

        self._topic = b'omniunibot'

        # Initialize ZMQ
        self._addr = bind
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.connect(self._addr)
        logger.debug(f"Client connect to {self._addr}")
        # wait for connection to be ready
        sleep(1)

    def send(self,
             channel: str,
             msg: str,
             title: Optional[str] = None,
             msgType: str = 'text',
             **kwargs):
        """Send message to OmniUniBotServer

        Args:
            channel (str): The channel to send message. If the channel name is not
                configured, the message will be disposed.
            msg (str): The message content.
            title (Optional[str], optional): Title of the message. Defaults to None.
            msgType (str, optional): Type of the message. Defaults to 'text'.
        """
        payload = {
            "channel": channel,
            "msgType": msgType,
            "msg": msg
        }
        if title:
            payload["title"] = title
        info = json.dumps(payload).encode('utf-8')
        self._socket.send_multipart([self._topic, info])
        logger.debug(f"Client sent msg {info}")
