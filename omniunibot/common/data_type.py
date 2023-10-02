from enum import Enum, auto
from abc import abstractmethod, abstractclassmethod, ABC
from dataclasses import dataclass
from typing import Optional, Dict
from pathlib import Path


class OmniUniBotPlatform(Enum):
    Slack = "Slack"
    Lark = "Lark"
    DingTalk = "DingTalk"
    WeChatWork = "WeChatWork"


class DictCompatibleADT(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractclassmethod
    def from_dict(cls):
        pass


@dataclass
class OmniUniBotChannelConfig(DictCompatibleADT):
    platform: OmniUniBotPlatform
    webhook: str
    secret: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "platform": self.platform.value,
            "webhook": self.webhook,
        }
        if self.secret is not None:
            d["secret"] = self.secret
        return d

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            OmniUniBotPlatform(d["platform"]),
            d["webhook"],
            d.get("secret", None),
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OmniUniBotChannelConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.platform == __value.platform,
                self.webhook == __value.webhook,
                self.secret == __value.secret,
            ]
        )


@dataclass
class OmniUniBotClientConfig(DictCompatibleADT):
    bind: str

    def to_dict(self) -> dict:
        return {"bind": self.bind}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["bind"])

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OmniUniBotClientConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.bind == __value.bind,
            ]
        )


@dataclass
class OmniUniBotServerConfig(DictCompatibleADT):
    bind: str
    interval: float

    def to_dict(self) -> dict:
        return {"bind": self.bind, "interval": self.interval}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["bind"], d["interval"])

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OmniUniBotServerConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.bind == __value.bind,
                self.interval == __value.interval,
            ]
        )


@dataclass
class OmniUniBotLoggingConfig(DictCompatibleADT):
    level: str = "DEBUG"
    dir: Path = Path.home() / "logs" / "omniunibot"

    def to_dict(self) -> dict:
        return {"level": self.level, "dir": str(self.dir.absolute())}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["level"], Path(d["dir"]))

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OmniUniBotLoggingConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.level == __value.level,
                self.dir == __value.dir,
            ]
        )


@dataclass
class OmniUniBotConfig(DictCompatibleADT):
    server: OmniUniBotServerConfig
    client: OmniUniBotClientConfig
    log: OmniUniBotLoggingConfig
    channel_groups: Dict[str, list[OmniUniBotChannelConfig]]

    def to_dict(self) -> dict:
        return {
            "server": self.server.to_dict(),
            "client": self.client.to_dict(),
            "log": self.log.to_dict(),
            "channel_groups": {k: [channel.to_dict() for channel in v] for k, v in self.channel_groups.items()},
        }

    @classmethod
    def from_dict(cls, d: dict):
        channel_groups = {}
        for k in d["channel_groups"].keys():
            channel_groups[k] = [
                OmniUniBotChannelConfig.from_dict(channel_config) for channel_config in d["channel_groups"][k]
            ]
        return cls(
            OmniUniBotServerConfig.from_dict(d["server"]),
            OmniUniBotClientConfig.from_dict(d["client"]),
            OmniUniBotLoggingConfig.from_dict(d["log"]) if "log" in d.keys() else OmniUniBotLoggingConfig(),
            channel_groups,
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OmniUniBotConfig):
            raise TypeError(f"{type(__value)}")
        return all(
            [
                self.server == __value.server,
                self.client == __value.client,
                self.log == __value.log,
                self.channel_groups == __value.channel_groups,
            ]
        )


class MsgType(Enum):
    Text = "Text"
    Image = "Image"


@dataclass
class Msg(DictCompatibleADT):
    channel_group: str
    msg_type: MsgType
    msg_content: dict

    def to_dict(self) -> dict:
        return {
            "channel_group": self.channel_group,
            "msg_type": self.msg_type.value,
            "msg_content": self.msg_content,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d["channel_group"],
            MsgType(d["msg_type"]),
            d["msg_content"],
        )
