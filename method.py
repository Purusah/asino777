from jsonrpcserver.aio import methods
from casino import Roulette777

roulette = Roulette777()




@methods.add
async def ping():
    return 'pong'


@methods.add
async def get_balance():
    return roulette.get_balance()

@methods.add
async def update_balance(**kwargs):
    amount = kwargs.get("amount")
    balance_returned = roulette.update_balance(amount)
    return balance_returned

