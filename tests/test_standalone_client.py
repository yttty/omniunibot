"""
Hot to run:
    1. python setup.py develop
    2. python test_standalone_client.py
"""

from omniunibot import OmniUniBotClient
from loguru import logger
from time import sleep

if __name__ == '__main__':

    client = OmniUniBotClient("tcp://*:58655")

    for i in range(1, 40):
        msgTitle = f"Test {i}"
        msgContent = f'Test {i} passed!'
        client.send(
            title=msgTitle,
            msg=msgContent
        )
        sleep(5)
