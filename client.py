from tornado import ioloop
from jsonrpcclient.tornado_client import TornadoClient
#from casino import get_balance


port = 8001
client = TornadoClient("http://localhost:8001/")

balance = {
    "amount": 137
}

async def get_balance():
    await client.request("get_balance")

async def update_balance():
    await client.request("update_balance", **balance)




ioloop.IOLoop.current().run_sync(update_balance)