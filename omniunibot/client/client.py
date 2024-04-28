import zmq
import json
from loguru import logger
from zmq.asyncio import Context
import time
import operator
from typing import Any, Dict
from typing import Optional, Union

from ..common.data_type import Msg, MsgType, OmniUniBotConfig
from ..common.constants import OMNI_ZMQ_TOPIC


class OmniUniBotClient:
    def __init__(
        self,
        bind: Optional[str] = None,
        config: Optional[OmniUniBotConfig] = None,
        quiet: bool = True,
    ) -> None:
        """Initialize OmniUniBot Client

        Args:
            bind (str): the bind addr
            config (OmniUniBotConfig): the config
            quiet (bool): set True to avoid print debug logs
        """
        # sanity check
        assert operator.xor(bind is not None, config is not None), "Must provide `bind` OR `config`"
        if config is not None:
            self._config = config
            self._addr = self._config.client.bind
            self._channel_groups = self._config.channel_groups
        else:
            self._config = None
            self._addr = bind
            self._channel_groups = None

        self._quiet = quiet

        # Initialize ZMQ
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.connect(self._addr)
        if not self._quiet:
            logger.debug(f"Client connect to {self._addr}")
        # wait for connection to be ready
        time.sleep(1)

    def _check_channel_configured(
        self,
        channel_group: str,
    ) -> bool:
        if self._channel_groups is not None:
            return channel_group in self._channel_groups.keys()
        else:
            return True

    def _fmt_msg(
        self,
        channel_group: str,
        msg_content: Dict[str, Any],
        msg_type: Union[str, MsgType],
    ) -> Optional[Msg]:
        """Validate and format message

        Args:
            channel_group (str): The channel to send message. If the channel name is not
                configured, the message will be disposed.
            msg_type (str): Type of the message. Defaults to 'Text'.
            msg_content (kwargs): ...
        """
        if type(msg_type) is str:
            msg_type = MsgType[msg_type]
        if self._check_channel_configured(channel_group):
            return Msg.from_dict(
                {
                    "channel_group": channel_group,
                    "msg_content": msg_content,
                    "msg_type": msg_type.name,
                }
            )
        else:
            logger.warning(f"Channel {channel_group} not configured.")
            return None

    def send(
        self,
        channel_group: str,
        msg_content: Dict[str, Any],
        msg_type: MsgType | str = "Auto",
    ):
        """Send message to OmniUniBotServer

        Args:
            channel_group (str): The channel to send message. If the channel name is not
                configured, the message will be disposed.
            msg_content (dict): ...
            msg_type (str): Type of the message. Defaults to 'Text'.
        """
        msg = self._fmt_msg(channel_group, msg_content, msg_type)
        if msg is not None:
            info = json.dumps(msg.to_dict()).encode("utf-8")
            self._socket.send_multipart([OMNI_ZMQ_TOPIC, info])
            if not self._quiet:
                logger.debug(f"Client sent msg {info}")

    async def send_async(
        self,
        channel_group: str,
        msg_content: Dict[str, Any],
        msg_type: MsgType | str = "Auto",
    ):
        """Async send message to OmniUniBotServer

        Args:
            channel_group (str): The channel to send message. If the channel name is not
                configured, the message will be disposed.
            msg_content (dict): ...
            msg_type (str): Type of the message. Defaults to 'Text'.
        """
        msg = self._fmt_msg(channel_group, msg_content, msg_type)
        if msg is not None:
            info = json.dumps(msg.to_dict()).encode("utf-8")
            await self._socket.send_multipart([OMNI_ZMQ_TOPIC, info])
            if not self._quiet:
                logger.debug(f"Client sent msg {info}")
