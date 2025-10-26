import asyncio
import json
import logging
import os
from typing import Any, Dict, List, TypeAlias

from aiohttp import web

from .connectors import DingTalkBot, LarkBot, SlackBot
from .data_type import ChannelConfig, Platform, ServerConfig

BotsDict: TypeAlias = Dict[str, List[DingTalkBot | LarkBot | SlackBot]]
logger = logging.getLogger("OMNIUNIBOT")


def load_config() -> ServerConfig:
    config_path = "/app/omni_config.json"
    try:
        config_data: dict[str, Any] = json.load(open(config_path, "r"))
        _debug = config_data.get("debug", False)
        _channel_groups = {}
        for group_name, group_channel_l in config_data["channel_groups"].items():
            _channel_groups[group_name] = [
                ChannelConfig(
                    Platform[str(_group_channel["platform"]).upper()],
                    _group_channel["webhook"],
                    _group_channel.get("secret", None),
                )
                for _group_channel in group_channel_l
            ]
        _server_config = ServerConfig(_channel_groups, _debug)
        logger.info(f"Config: {_server_config.to_dict()}")
        return _server_config
    except Exception as e:
        logger.critical(f"Failed to load config from {config_path}, error: {e}")
        os._exit(-1)


def init_bots(config: ServerConfig) -> BotsDict:
    bots_d: BotsDict = {}
    for channel_group_name, channel_group_config in config.channel_groups.items():
        bots_d[channel_group_name] = []
        for channel_config in channel_group_config:
            if channel_config.platform == Platform.SLACK:
                bots_d[channel_group_name].append(SlackBot(channel_config.webhook))
            elif channel_config.platform == Platform.DINGTALK:
                if channel_config.secret is not None:
                    bots_d[channel_group_name].append(DingTalkBot(channel_config.webhook, channel_config.secret))
                else:
                    logger.error(f"Fail to initialize DingTalkBot in group {channel_group_name} without secret.")
            elif channel_config.platform == Platform.LARK:
                if channel_config.secret is not None:
                    bots_d[channel_group_name].append(LarkBot(channel_config.webhook, channel_config.secret))
                else:
                    logger.error(f"Fail to initialize LarkBot in group {channel_group_name} without secret.")
            else:
                logger.error(f"Fail to initialize {channel_config.to_dict()} in group {channel_group_name}")
        logger.info(
            f"Initialized {len(bots_d[channel_group_name])} destinations in channel group {channel_group_name}"
        )
    logger.info(f"Total {len(bots_d)} channel groups ready.")
    return bots_d


routes = web.RouteTableDef()


@routes.post("/push")
async def handle_post_push(request: web.Request) -> web.Response:
    try:
        payload: dict = await request.json()
    except json.JSONDecodeError as e:
        return web.json_response({"error_msg": f"JSON decode error. {e}"}, status=400)

    channel_group: str = payload.get("channel_group", "")
    if not channel_group:
        return web.json_response(data={"error_msg": "Missing mandatory param channel_group."}, status=400)
    elif channel_group not in bots_d:
        return web.json_response(data={"error_msg": f"Channel group {channel_group} not found."}, status=404)

    msg_text: str = payload.get("msg_text", "")
    if not msg_text:
        return web.json_response(data={"error_msg": "Missing mandatory param msg_text."}, status=400)
    msg_content: Dict[str, Any] = {"text": msg_text}

    mention_all: bool = payload.get("mention_all", False)

    tasks: List[asyncio.Task] = []
    async with asyncio.TaskGroup() as tg:
        for bot in bots_d[channel_group]:
            tasks.append(tg.create_task(bot.send(msg_content=msg_content, mention_all=mention_all)))
    success = all([task.result() for task in tasks])
    if success:
        return web.json_response(data={"result": "SUCCESS"}, status=200)
    else:
        return web.json_response(data={"result": "FAILED"}, status=500)


@routes.get("/groups")
async def handle_get_groups(request: web.Request) -> web.Response:
    return web.json_response(data={"groups": list(bots_d.keys())}, status=200)


logger = logging.getLogger("UPUSH")
logger.setLevel(logging.DEBUG)
config: ServerConfig = load_config()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
)
handler.setLevel(logging.DEBUG if config.debug else logging.INFO)
logger.addHandler(handler)
bots_d: BotsDict = init_bots(config)
app = web.Application()
app.add_routes(routes)
