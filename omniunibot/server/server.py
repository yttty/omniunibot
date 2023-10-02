import os
import zmq
import json
import asyncio
from loguru import logger
from zmq.asyncio import Context
import traceback
from typing import Union, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

from .wrapper.dingtalk import DingTalkBot
from .wrapper.lark import LarkBot
from .wrapper.slack import SlackBot
from .wrapper.base import BaseBot
from ..common.data_type import OmniUniBotConfig, OmniUniBotPlatform, OmniUniBotChannelConfig, MsgType, Msg
from ..common.constants import OMNI_ZMQ_TOPIC


class OmniUniBotServer:
    def __init__(self, config: OmniUniBotConfig) -> None:
        """Initialize OmniUniBot Server

        Args:
            config (dict): the config dict

        Raises:
            ValueError: Raised there is no such channel in config
        """
        assert isinstance(config, OmniUniBotConfig), "Invalid config"
        self._config = config
        self._init_logger()
        self._init_bots()

        # Initialize ZMQ
        self._addr = self._config.server.bind
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))

        # Initialize loop
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

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

    def _get_bot(self, channel_config: OmniUniBotChannelConfig) -> Optional[Union[LarkBot, DingTalkBot, SlackBot]]:
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

    def _bulk_send(
        self,
        channel_group_name: str,
        msg_type: MsgType,
        msg_content: dict,
    ):
        """_summary_

        Args:
            channel_group_name (str): _description_
            msg_type (MsgType): _description_
        """
        executors = []
        with ThreadPoolExecutor(max_workers=len(self._bots[channel_group_name])) as executor:
            for bot in self._bots[channel_group_name]:
                executors.append(
                    executor.submit(
                        bot.send,
                        msg_type=msg_type,
                        msg_content=msg_content,
                    )
                )

    async def _start_server(self):
        self._socket.bind(self._addr)
        logger.info(f"Server bind to {self._addr}")
        while True:
            try:
                mtPart = await self._socket.recv_multipart()
                if mtPart[0] == OMNI_ZMQ_TOPIC:
                    part: dict = json.loads(mtPart[1].decode("utf-8"))
                    msg = Msg.from_dict(part)
                    if msg.channel_group not in self._bots.keys():
                        raise ValueError(f"No such channel {msg.channel_group}")
                    self._bulk_send(
                        channel_group_name=msg.channel_group,
                        msg_type=msg.msg_type,
                        msg_content=msg.msg_content,
                    )
            except KeyboardInterrupt:
                logger.info("Bye")
                exit(0)
            except Exception as e:
                logger.error(f"Server encounter {str(e)}. Data={part}")
                logger.debug(traceback.format_exc())
            finally:
                await asyncio.sleep(self._config.server.interval)

    def start(self):
        asyncio.ensure_future(self._start_server(), loop=self._loop)
        self._loop.run_forever()
