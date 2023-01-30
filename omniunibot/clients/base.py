from loguru import logger


class BaseBot:
    """
    Base class for bot, defines interfaces
    """

    def _onSuccessResponse(self, response=None) -> int:
        raise NotImplementedError

    def _onErrorResponse(self, res) -> int:
        raise NotImplementedError

    def generatePayload(self, msgtype: str, **kwargs):
        raise NotImplementedError

    def sendMessage(self, payload: dict):
        raise NotImplementedError

    def sendQuickMessage(self, msg: str):
        raise NotImplementedError
