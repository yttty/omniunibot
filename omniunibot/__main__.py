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

    parser.set_defaults(config=f'{os.environ["HOME"]}/configs/omniunibot.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    logger.debug(f'Config path: {args.config}')

    server = OmniUniBotServer(args.config)
    server.run()
