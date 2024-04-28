import os
import zmq
import json
import asyncio
from loguru import logger
from zmq.asyncio import Context
import traceback
from typing import Dict, Any, Deque
from pathlib import Path
from collections import deque

from ..connector.dingtalk import DingTalkBot
from ..connector.lark import LarkBot
from ..connector.slack import SlackBot
from ..connector.base import BaseBot
from ..common.data_type import OmniUniBotConfig, OmniUniBotPlatform, OmniUniBotChannelConfig, MsgType, Msg
from ..common.constants import OMNI_ZMQ_TOPIC


class OmniUniBotServer:
    def __init__(self, config: OmniUniBotConfig | str | Path | None) -> None:
        """Initialize OmniUniBot Server

        Args:
            config (dict): the config dict

        Raises:
            ValueError: Raised there is no such channel in config
        """

        if config is None:
            self._config = OmniUniBotConfig.from_dict(
                json.load(open(Path.home() / "configs" / "omniunibot.json", "r"))
            )
        elif isinstance(config, str) or isinstance(config, Path):
            self._config = OmniUniBotConfig.from_dict(json.load(open(config, "r")))
        elif isinstance(config, OmniUniBotConfig):
            self._config = config
        else:
            raise TypeError("Invalid config")

        self._init_logger()
        logger.debug(f"Config: {self._config.to_dict()}")
        self._init_bots()
        self._msg_queue:Deque[Msg] = deque()

        # Initialize ZMQ
        self._addr = self._config.server.bind
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))

    def _init_logger(self):
        handlers_cfg = []
        assert self._config.log.level in ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
        log_file_handler_cfg = dict(
            sink=str(self._config.log.dir / ("omniunibot.server" + ".{time:YYYY-MM-DD}" + ".log")),
            level=self._config.log.level,
            rotation="00:00",
        )
        handlers_cfg.append(log_file_handler_cfg)
        logger.configure(handlers=handlers_cfg)

    def _get_bot(self, channel_config: OmniUniBotChannelConfig) -> LarkBot | DingTalkBot | SlackBot | None:
        if channel_config.platform == OmniUniBotPlatform.Slack:
            return SlackBot(channel_config.webhook)
        elif channel_config.platform == OmniUniBotPlatform.DingTalk:
            return DingTalkBot(channel_config.webhook, channel_config.secret)
        elif channel_config.platform == OmniUniBotPlatform.Lark:
            return LarkBot(channel_config.webhook, channel_config.secret)
        else:
            return None

    def _init_bots(self):
        # Initialize bots
        self._bots: Dict[str, list[BaseBot]] = {}
        for channel_group_name, channel_group_config in self._config.channel_groups.items():
            self._bots[channel_group_name] = []
            for channel_config in channel_group_config:
                bot = self._get_bot(channel_config=channel_config)
                if bot is not None:
                    self._bots[channel_group_name].append(bot)
                else:
                    logger.error(f"Fail to initialize {channel_config.to_dict()} in group {channel_group_name}")
            logger.info(
                f"Initialized {len(self._bots[channel_group_name])} destinations in channel group {channel_group_name}"
            )
        logger.info(f"Total {len(self._bots)} channel groups ready.")

    async def _bulk_send(
        self,
        channel_group_name: str,
        msg_content: Dict[str, Any],
        msg_type: MsgType,
    ):
        """_summary_

        Args:
            channel_group_name (str): _description_
            msg_type (MsgType): _description_
        """
        for bot in self._bots[channel_group_name]:
            asyncio.create_task(bot.send(msg_content=msg_content, msg_type=msg_type))

    async def _pull_zmq(self):
        self._socket.bind(self._addr)
        logger.info(f"Server bind to {self._addr}")
        while True:
            try:
                mtPart = await self._socket.recv_multipart()
                if mtPart[0] == OMNI_ZMQ_TOPIC:
                    part: dict = json.loads(mtPart[1].decode("utf-8"))
                    msg = Msg.from_dict(part)
                    if msg.channel_group not in self._bots.keys():
                        logger.warning(f"Ignore msg because of no such channel. Channel={msg.channel_group} Msg={msg.to_dict()}")
                    else:
                        self._msg_queue.append(msg)
            except Exception as e:
                logger.error(f"_pull_zmq encounter {str(e)}. Data={part}")
                logger.debug(traceback.format_exc())

    async def _send_msg(self):
        while True:
            try:
                if len(self._msg_queue) > 0:
                    msg = self._msg_queue.popleft()
                    asyncio.create_task(
                        self._bulk_send(
                            channel_group_name=msg.channel_group,
                            msg_content=msg.msg_content,
                            msg_type=msg.msg_type,
                        )
                    )
            except Exception as e:
                logger.error(f"_send_msg encounter {str(e)}.")
                logger.debug(traceback.format_exc())
            finally:
                await asyncio.sleep(self._config.server.interval)

    async def start(self):
        try:
            async with asyncio.TaskGroup() as tg:
                _ = tg.create_task(self._pull_zmq())
                _ = tg.create_task(self._send_msg())
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            logger.info("Stop {}. Bye.", self.__class__.__name__)
            exit(0)
