import zmq
import json
from loguru import logger
from zmq import Context
from time import sleep


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
        self._socket.bind(self._addr)
        logger.debug(f"Client bind to {self._addr}")
        # wait for connection is ready
        sleep(1)

    def send(self, title, msg):
        info = json.dumps({
            "title": title,
            "msg": msg
        }).encode('utf-8')
        self._socket.send_multipart([self._topic, info])
        logger.debug(f"Client sent msg {info}")
