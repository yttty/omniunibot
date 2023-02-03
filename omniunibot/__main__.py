import argparse
import os

from loguru import logger
from omniunibot import OmniUniBotServer


def parse_args():
    parser = argparse.ArgumentParser(
        prog='omniunibot',
        description='Start a omniunibot server.',
        epilog='Doc: https://github.com/yttty/omniunibot'
    )

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

    server = OmniUniBotServer(args.config, args.channel)
    server.run()
