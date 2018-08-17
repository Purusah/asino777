from jsonrpcserver.aio import methods
from block import Block

# block = Block()
# roulette = block.deploy_contract()
# account = block.eth.defaultAccount

class Bot(object):
    def __init__(self):
        self.blockchain = Block()
        # by default it is Roulette contract
        self.contract = self.blockchain.deploy_contract()
        self.owner_account = self.blockchain.eth.defaultAccount
        self.accounts = self.blockchain.eth.accounts

    @methods.add
    async def ping(self):
        return "pong"

    @methods.add
    async def get_owner(self):
        return self.owner_account


bot = Bot()


@methods.add
async def get_balance():
    return roulette.get_balance()


@methods.add
async def update_balance(**kwargs):
    amount = kwargs.get("amount")
    balance_returned = roulette.update_balance(amount)
    return balance_returned


@methods.add
async def bet_on_number(**kwargs):
    amount = kwargs.get("amount")
    number = kwargs.get("number")
    tx_receipt = roulette.bet_on_number(number, amount)
    return tx_receipt


@methods.add
async def client_get_balance(**kwargs):
    address = kwargs.get("address")
    amount = roulette.client_get_balance(address)
    return amount


@methods.add
async def get_bet(**kwargs):
    number = kwargs.get("number")
    bet = roulette.get_bet(number)
    return bet


@methods.add
async def spin_wheel(**kwargs):
    address = kwargs.get("address")
    amount = roulette.spin_wheel(address)
    return amount




