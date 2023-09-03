import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from loguru import logger
import traceback

from ...common.data_type import MsgType


class BaseBot(ABC):
    """
    Base class for bot, defines interfaces
    """

    def _new_uuid(self):
        return str(uuid.uuid4())

    @abstractmethod
    def _on_success_response(self, resp=None) -> None:
        pass

    @abstractmethod
    def _on_error_response(self, resp) -> None:
        pass

    @abstractmethod
    def _on_response(self, res) -> None:
        pass

    @abstractmethod
    def _generate_payload(self, msg_type: MsgType, **kwargs):
        pass

    @abstractmethod
    def _send_image(self, img_path: Union[str, Path], **kwargs):
        pass

    @abstractmethod
    def _send_text(self, text: str, **kwargs):
        pass

    def send(self, msg_type: MsgType, msg_content: dict):
        try:
            msg_id: str = self._new_uuid()
            if msg_type == MsgType.Text:
                assert (
                    "text" in msg_content.keys() and msg_content["text"] is not None
                ), "`text` is required in `msg_content` when `msg_type` == MsgType.Text"
                self._send_text(msg_id=msg_id, **msg_content)
            elif msg_type == MsgType.Image:
                assert (
                    "img_path" in msg_content.keys() and msg_content["img_path"] is not None
                ), "`img_path` is required in `msg_content` when `msg_type` == MsgType.Image"
                self._send_image(msg_id=msg_id, **msg_content)
            else:
                raise NotImplementedError
        except NotImplementedError:
            logger.error(f"Send {msg_type} is not supported yet.")
        except Exception as e:
            logger.error(f"{e.__class__.__name__} - {str(e)}")
            logger.debug(f"{traceback.format_exc()}")
