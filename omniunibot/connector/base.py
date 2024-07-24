import asyncio
import inspect
import traceback
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, Literal, Union

from loguru import logger

from ..common.data_type import MsgType


class BaseBot(ABC):
    """
    Base class for bot, defines interfaces
    """

    _platform = None

    def __init__(
        self,
        on_success: Literal["log", "nop"] = "nop",
        on_failure: Literal["log", "nop"] | Callable[..., None] = "log",
        debug: bool = False,
    ) -> None:
        assert on_success in ["log", "nop"]
        self._on_success = on_success
        if isinstance(on_failure, Callable):
            if inspect.iscoroutinefunction(on_failure):
                self._on_failure = on_failure
            else:
                raise TypeError("`on_failure` should be coroutine")
        else:
            assert on_failure in ["trace", "log", "nop"]
            self._on_failure = on_failure
        self._debug = debug

    async def _on_success_response(self, msg_id: str) -> None:
        match self._on_success:
            case "log":
                logger.info("Successully sent message {} to {}.", msg_id, self._platform)

    async def _on_error_response(self, msg_id: str, err_data: Any) -> None:
        match self._on_success:
            case "log":
                logger.error("Fail to send message {} to {}. ErrData={}", msg_id, self._platform, str(err_data))
            case "nop":
                pass
            case _:
                try:
                    asyncio.create_task(self._on_failure(err_data))
                except Exception as e:
                    logger.error("{} in dealing with error response! Msg={}", e.__class__.__name__, str(e))

    async def send(self, msg_content: Dict[str, Any], msg_type: MsgType | str = "Auto", **kwargs):
        try:
            msg_id: str = str(uuid.uuid4().hex)

            # decide msg_type
            if msg_type == "Auto" or msg_type == MsgType.Auto:
                if "text" in msg_content:
                    msg_type = MsgType.Text
                elif "markdown" in msg_content:
                    msg_type = MsgType.Markdown
                elif "img_path" in msg_content:
                    msg_type = MsgType.Image
                else:
                    raise ValueError("Fail to auto decide msg_type!")
            elif isinstance(msg_type, str):
                msg_type == MsgType[msg_type]
            elif not isinstance(msg_type, MsgType):
                raise TypeError("Invalid `msg_type`")

            # send msg
            if msg_type == MsgType.Text:
                assert (
                    msg_text := msg_content.get("text", None)
                ), "`text` is required in `msg_content` when `msg_type` == MsgType.Text"
                if self._debug:
                    logger.debug(f"Receive text message: {msg_text}")
                rsp = await self._send_text(msg_text)
            elif msg_type == MsgType.Markdown:
                assert (
                    msg_md := msg_content.get("markdown", None)
                ), "`markdown` is required in `msg_content` when `msg_type` == MsgType.Markdown"
                if self._debug:
                    logger.debug(f"Receive markdown message: {msg_md}")
                rsp = await self._send_markdown(msg_md)
            elif msg_type == MsgType.Image:
                assert (
                    img_path := msg_content.get("img_path", None)
                ), "`img_path` is required in `msg_content` when `msg_type` == MsgType.Image"
                if self._debug:
                    logger.debug(f"Receive img message: {img_path}")
                rsp = await self._send_image(img_path)
            else:
                raise NotImplementedError

            # on response
            await self._on_response(msg_id, rsp)
        except NotImplementedError:
            await self._on_error_response(msg_id, f"Send {msg_type} is not supported yet. msg_id={msg_id}")
        except Exception as e:
            await self._on_error_response(msg_id, {"exception": e.__class__.__name__, "exception_msg": str(e)})

    @abstractmethod
    async def _on_response(self, msg_id: str, rsp: Any = None) -> None:
        pass

    @abstractmethod
    async def _send_text(self, msg_text: str) -> Any | None:
        pass

    async def _send_markdown(self, msg_md: str) -> Any | None:
        raise NotImplementedError

    async def _send_image(self, img_path: str | Path) -> Any | None:
        raise NotImplementedError
