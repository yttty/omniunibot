import argparse
import asyncio

from ..common.data_type import OmniUniBotConfig
from .server import OmniUniBotServer


def parse_args():
    parser = argparse.ArgumentParser(
        prog="omniunibot",
        description="Start a omniunibot server.",
        epilog="Doc: https://github.com/yttty/omniunibot",
    )
    parser.add_argument("-c", "--config", dest="config", help="Path of config file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = OmniUniBotServer(args.config)
    asyncio.run(server.start())
