import zmq
import json
from loguru import logger
from zmq import Context

from concurrent.futures import ThreadPoolExecutor

from .wrapper.dingtalk import DingTalkBot
from .wrapper.wecom import WeComBot
from .wrapper.feishu import FeishuBot


class OmniUniBotServer:
    def __init__(self,
                 configPath: str,
                 channel: str) -> None:
        """Initialize OmniUniBot Server

        Args:
            config (dict): the config dict
            channel (str): the channel to send message

        Raises:
            ValueError: Raised there is no such channel in config
        """
        try:
            self._config = json.load(open(configPath, 'r'))
        except Exception as e:
            logger.error(f"Failed to open config file {configPath}")
            exit(-1)

        try:
            self._channel = channel
            if channel not in self._config["channels"]:
                raise ValueError('No such channel in config file')
        except ValueError as e:
            logger.error(str(e))
            exit(-1)

        self._topic = b'omniunibot'

        # Initialize ZMQ
        self._addr = self._config['bind']
        self._ctx = Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))

        # Initialize bots
        self.bots = []
        for targetChannelConfig in self._config["channels"][self._channel]:
            if targetChannelConfig['platform'] == "feishu":
                bot = FeishuBot(webhook=targetChannelConfig['webhook'],
                                secret=targetChannelConfig['secret'])
            elif targetChannelConfig['platform'] == "dingtalk":
                bot = DingTalkBot(webhook=targetChannelConfig['webhook'],
                                  secret=targetChannelConfig['secret'])
            elif targetChannelConfig['platform'] == "wecom":
                bot = WeComBot(webhook=targetChannelConfig['webhook'])
            else:
                raise KeyError("Unknown platform {}".format(
                    targetChannelConfig['platform']))
            self.bots.append(bot)

    def bulkSend(self, msg: str):
        executors = []
        with ThreadPoolExecutor(max_workers=len(self.bots)) as executor:
            for bot in self.bots:
                executors.append(executor.submit(bot.sendQuickMessage, msg))

    def run(self):
        self._socket.connect(self._addr)
        logger.debug(f"Server connect to {self._addr}")
        while True:
            try:
                info = json.loads(self._socket.recv_multipart()[
                                  1].decode('utf-8'))
                msgStr = "{}\n{}\n".format(
                    info['title'], '-' * len(info['title']))
                msgStr += info['msg']
                self.bulkSend(msgStr)
            except Exception as e:
                logger.error(str(e))
                pass
