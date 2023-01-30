"""
Hot to run:
    1. python setup.py install
    2. python test_send.py --config $HOME/configs/omniunibot-test.json --platform feishu
"""


import argparse
import json
from pprint import pprint

from loguru import logger
from omniunibot import FeishuBot, DingTalkBot, WXWorkBot


class Tester:
    def __init__(self, platform: str):
        self.platform = platform

        if args.platform == "feishu":
            self.bot = FeishuBot(cfg['feishu']['token'],
                                 cfg['feishu']['secret'])
        elif args.platform == "ding":
            self.bot = DingTalkBot(cfg['ding']['token'],
                                   cfg['ding']['secret'])
        elif args.platform == "wxwork":
            self.bot = WXWorkBot(cfg['wxwork']['token'])
        else:
            raise ValueError('Incorrect platform')

    def run(self):
        self.bot.sendQuickMessage('Test Passed')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config',
        dest='config',
        help='Path of config file',
        required=True)

    parser.add_argument(
        '--platform',
        dest='platform',
        help='Choose platform (feishu, ding, wxwork)')

    parser.set_defaults(platform='feishu')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    logger.configure(
        handlers=[dict(sink='logs/test.log',
                       level='INFO',
                       rotation="00:00")]
    )

    msg = "Bots Tester"
    print(msg + "\n" + '-' * len(msg))

    cfg = json.load(open(args.config))
    print('Config:')
    pprint(cfg)
    print()

    print("Platform:", args.platform)

    tester = Tester(args.platform)
    tester.run()
