from tornado import ioloop
from jsonrpcclient.tornado_client import TornadoClient
#from casino import get_balance


port = 8001
client = TornadoClient("http://localhost:8001/")


async def get_balance():
    await client.request("get_balance")

async def update_balance():
    await client.request("update_balance", **balance)

async def test_ping():
    await client.request("ping")


# async def main():
#     b = await get_balance()
#     #assert(b == 274)
#     p = await test_ping()
#     #assert(p == "pong")
#
# ioloop.IOLoop.current().run_sync(main)