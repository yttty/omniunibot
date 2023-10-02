import argparse
import json
from pathlib import Path

from loguru import logger
from .server import OmniUniBotServer
from ..common.data_type import OmniUniBotConfig


def parse_args():
    parser = argparse.ArgumentParser(
        prog="omniunibot",
        description="Start a omniunibot server.",
        epilog="Doc: https://github.com/yttty/omniunibot",
    )
    parser.add_argument("--config", dest="config", help="Path of config file")
    parser.set_defaults(config=Path.home() / "configs" / "omniunibot.json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logger.debug(f"Config path: {args.config}")
    try:
        config = OmniUniBotConfig.from_dict(json.load(open(args.config, "r")))
    except Exception as e:
        logger.error(f"Failed to open config file {args.config}. Reason: {str(e)}")
        exit(-1)
    server = OmniUniBotServer(config)
    server.start()
