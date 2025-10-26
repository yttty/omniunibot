import logging
import traceback
import uuid
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, Literal

from slack_sdk.webhook import WebhookResponse

logger = logging.getLogger("OMNIUNIBOT")


class MsgType(Enum):
    Text = auto()
    Markdown = auto()
    Image = auto()


class BaseBot(ABC):
    """
    Base class for bot, defines interfaces
    """

    _platform: str = ""

    def __init__(
        self,
        on_success: Literal["log", "nop"] = "nop",
        on_failure: Literal["trace", "log", "nop"] = "log",
    ) -> None:
        assert on_success in ["log", "nop"]
        self._on_success = on_success
        assert on_failure in ["trace", "log", "nop"]
        self._on_failure = on_failure

    async def _on_success_response(self, msg_id: str) -> None:
        match self._on_success:
            case "log":
                logger.info("Successully sent message {} to {}.".format(msg_id, self._platform))

    async def _on_error_response(self, msg_id: str, err_msg: str) -> None:
        match self._on_failure:
            case "log" | "trace":
                logger.error("Fail to send message {} to {}. ErrMsg={}".format(msg_id, self._platform, err_msg))
                if self._on_failure == "trace":
                    logger.debug(traceback.format_exc())
            case "nop":
                pass

    async def send(
        self,
        msg_content: Dict[str, Any],
        mention_all: bool = False,
    ) -> bool:
        msg_id: str = str(uuid.uuid4().hex)
        if "text" in msg_content:
            msg_type = MsgType.Text
            msg_text: str = str(msg_content.get("text", "(None)"))
            logger.debug(f"Receive text message: {msg_text} / mention_all={mention_all}")
        elif "markdown" in msg_content:
            msg_type = MsgType.Markdown
            msg_md: str = str(msg_content.get("markdown", "(*None*)"))
            logger.debug(f"Receive markdown message: {msg_md} / mention_all={mention_all}")
        elif "img_b64" in msg_content:
            msg_type = MsgType.Image
            img_b64: bytes = msg_content.get("img_b64", b"")
            logger.debug(f"Receive base64 encoded image / mention_all={mention_all}")
        else:
            logger.error("Failed to auto determine msg_type!")
            return False

        try:
            match msg_type:
                case MsgType.Text:
                    rsp = await self._send_text(msg_text, mention_all)  # type: ignore
                case MsgType.Markdown:
                    rsp = await self._send_markdown(msg_md, mention_all)  # type: ignore
                case MsgType.Image:
                    rsp = await self._send_image(img_b64, mention_all)  # type: ignore

            if rsp is None:
                await self._on_error_response(msg_id, "")
                return False
            else:
                success = await self._is_success_response(rsp)
                if success:
                    await self._on_success_response(msg_id)
                    return True
                else:
                    await self._on_error_response(msg_id, rsp.body if isinstance(rsp, WebhookResponse) else str(rsp))
                    return False
        except NotImplementedError:
            await self._on_error_response(msg_id, f"Send {msg_type} is not supported yet. msg_id={msg_id}")
            return False
        except Exception as e:
            await self._on_error_response(msg_id, str(e))
            return False

    @abstractmethod
    async def _is_success_response(self, rsp: dict[str, Any]) -> bool:
        pass

    async def _send_text(self, text: str, mention_all: bool) -> dict[str, Any]:
        raise NotImplementedError

    async def _send_markdown(self, msg_md: str, mention_all: bool) -> dict[str, Any]:
        raise NotImplementedError

    async def _send_image(self, img_b64: bytes, mention_all: bool) -> dict[str, Any]:
        raise NotImplementedError
