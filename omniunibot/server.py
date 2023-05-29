import zmq
import json
import asyncio
from loguru import logger
from zmq.asyncio import Context
from traceback import format_exc

from concurrent.futures import ThreadPoolExecutor

from .wrapper.dingtalk import DingTalkBot
from .wrapper.wecom import WeComBot
from .wrapper.feishu import FeishuBot
from .wrapper.slack import SlackBot


class OmniUniBotServer:
    def __init__(self,
                 configPath: str) -> None:
        """Initialize OmniUniBot Server

        Args:
            config (dict): the config dict

        Raises:
            ValueError: Raised there is no such channel in config
        """
        try:
            self._config = json.load(open(configPath, 'r'))
        except Exception as e:
            logger.error(f"Failed to open config file {configPath}")
            exit(-1)

        try:
            self._channels = self._config["channels"]
            if len(self._channels) == 0:
                logger.error('No channels in config')
                exit(-1)
        except ValueError as e:
            logger.error(str(e))
            exit(-1)
        except KeyError as e:
            logger.error(str(e))
            exit(-1)

        self._topic = b'omniunibot'

        # Initialize ZMQ
        self._addr = self._config['bind']
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))

        # Initialize asyncio
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Initialize bots
        self.bots = {}
        for channel in self._channels.keys():
            self.bots[channel] = []
            for targetChannelConfig in self._config["channels"][channel]:
                if targetChannelConfig['platform'] == "feishu":
                    bot = FeishuBot(webhook=targetChannelConfig['webhook'],
                                    secret=targetChannelConfig['secret'])
                elif targetChannelConfig['platform'] == "dingtalk":
                    bot = DingTalkBot(webhook=targetChannelConfig['webhook'],
                                      secret=targetChannelConfig['secret'])
                elif targetChannelConfig['platform'] == "wecom":
                    bot = WeComBot(webhook=targetChannelConfig['webhook'])
                elif targetChannelConfig['platform'] == "slack":
                    bot = SlackBot(webhook=targetChannelConfig['webhook'])
                else:
                    raise KeyError("Unknown platform {}".format(
                        targetChannelConfig['platform']))
                self.bots[channel].append(bot)
            logger.info(
                f"Initialized {len(self.bots[channel])} destinations in channel {channel}")
        logger.info(f"Total {len(self.bots)} channels ready.")

    def _bulkSend(self,
                  channel: str,
                  msg: str,
                  msgType: str):
        """_summary_

        Args:
            channel (str): _description_
            msg (str): _description_
            msgType (str): _description_
        """
        executors = []
        with ThreadPoolExecutor(max_workers=len(self.bots[channel])) as executor:
            for bot in self.bots[channel]:
                executors.append(executor.submit(bot.sendQuickMessage, msg))

    async def _startServer(self):
        self._socket.bind(self._addr)
        logger.info(f"Server bind to {self._addr}")
        while True:
            try:
                mtPart = await self._socket.recv_multipart()
                info = json.loads(mtPart[1].decode('utf-8'))

                logger.debug(f"Server receive: {info}")

                if info['msgType'] not in ['text']:
                    raise NotImplementedError(
                        f"Unsupported message type {info['msgType']}")

                if info['channel'] not in self.bots.keys():
                    raise ValueError(f"No such channel {self.bots}")

                msgStr = ""
                if "title" in info.keys():
                    msgStr += "{}\n{}\n".format(
                        info['title'], '-' * len(info['title']))
                msgStr += info['msg']
                self._bulkSend(channel=info['channel'],
                               msg=msgStr,
                               msgType=info['msgType'])
            except KeyboardInterrupt:
                logger.info('Bye')
                exit(0)
            except Exception as e:
                logger.error(format_exc())
                pass

    def run(self):
        asyncio.ensure_future(self._startServer(), loop=self.loop)
        self.loop.run_forever()
