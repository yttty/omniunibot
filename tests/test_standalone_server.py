"""
Hot to run:
    1. python setup.py develop
    2. python test_standalone_server.py --config $HOME/configs/omniunibot.json
"""


import argparse
import json
import os

from loguru import logger
from omniunibot import OmniUniBotServer


class Tester:
    def __init__(self, config: str):
        self.server = OmniUniBotServer(config)

    def run(self):
        self.server.run()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config',
        dest='config',
        help='Path of config file')

    parser.set_defaults(config=f'{os.environ["HOME"]}/configs/omniunibot.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    logger.debug(f'Config path: {args.config}')

    tester = Tester(args.config)
    tester.run()
