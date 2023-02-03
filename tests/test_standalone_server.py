"""
Hot to run:
    1. python setup.py develop
    2. python test_standalone_server.py --channel test-feishu-channel --config $HOME/configs/omniunibot.json
"""


import argparse
import json
import os

from loguru import logger
from omniunibot import OmniUniBotServer


class Tester:
    def __init__(self, config: str, channel: str):
        self.channel = channel
        self.server = OmniUniBotServer(config, self.channel)

    def run(self):
        self.server.run()


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

    logger.debug(f'Config path: {args.config}')
    logger.debug(f"Channel: {args.channel}")

    tester = Tester(args.config, args.channel)
    tester.run()
