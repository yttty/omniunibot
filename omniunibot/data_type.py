from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional


class Platform(Enum):
    SLACK = auto()
    LARK = auto()
    DINGTALK = auto()


@dataclass
class ChannelConfig:
    platform: Platform
    webhook: str
    secret: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "platform": self.platform.name,
            "webhook": self.webhook,
        }
        if self.secret is not None:
            d["secret"] = self.secret
        return d

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ChannelConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.platform == __value.platform,
                self.webhook == __value.webhook,
                self.secret == __value.secret,
            ]
        )


@dataclass
class ServerConfig:
    channel_groups: Dict[str, list[ChannelConfig]]
    debug: bool

    def to_dict(self) -> dict:
        return {
            "channel_groups": {k: [channel.to_dict() for channel in v] for k, v in self.channel_groups.items()},
            "debug": self.debug,
        }

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ServerConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.channel_groups == __value.channel_groups,
                self.debug == __value.debug,
            ]
        )
