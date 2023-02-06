"""
Hot to run:
    1. python setup.py develop
    2. python test_standalone_client.py
"""

from omniunibot import OmniUniBotClient
from loguru import logger
from time import sleep
import typer

app = typer.Typer()


@app.command()
def runTest(channel: str = typer.Argument('test-feishu-channel'),
            bind: str = "tcp://*:58655"):
    client = OmniUniBotClient(bind)
    for i in range(1, 3):
        msgTitle = f"Test {i}"
        msgContent = f'Test {i} passed!'
        client.send(
            channel=channel,
            title=msgTitle,
            msg=msgContent
        )
        sleep(3)


if __name__ == '__main__':
    app()
