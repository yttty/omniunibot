import pytest

from omniunibot.common.data_type import Msg, MsgType


def test_msg_adt():
    msg_dict = {
        "channel_group": "test_channels",
        "msg_type": "Text",
        "msg_content": {"text": "`test_dingtalkbot_1` Pass"},
        "mention_all": True,
    }
    assert Msg.from_dict(msg_dict).to_dict() == msg_dict
