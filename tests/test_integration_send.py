"""
Hot to run:
    1. python setup.py develop
    2. python test_integration_send.py --channel test-channels --config $HOME/configs/omniunibot.json
"""


import argparse
import json
import os
from pprint import pprint

from loguru import logger
from omniunibot import FeishuBot, DingTalkBot, WeComBot, OmniUniBotServer


class Tester:
    def __init__(self, config: str, channel: str):
        self.channel = channel
        self.server = OmniUniBotServer(config, self.channel)

    def run(self):
        self.server._bulkSend('Test Passed')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config',
        dest='config',
        help='Path of config file')

    parser.add_argument(
        '--channel',
        dest='channel',
        help='The channel to send message',
        required=True)

    parser.set_defaults(config=f'{os.environ["HOME"]}/configs/omniunibot.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    logger.configure(
        handlers=[dict(sink='logs/test.log',
                       level='DEBUG',
                       rotation="00:00")]
    )

    msg = "Bots Tester"
    logger.debug('-' * len(msg))
    logger.debug(msg)
    logger.debug('-' * len(msg))
    logger.debug(f'Config path: {args.config}')
    logger.debug(f"Channel: {args.channel}")

    tester = Tester(args.config, args.channel)
    tester.run()
