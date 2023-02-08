from omniunibot import OmniUniBotClient

client = OmniUniBotClient("tcp://*:58655")
client.send(
    title="msgTitle",
    msg="msgContent"
)