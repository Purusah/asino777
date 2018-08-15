from web3 import Web3
from solc import compile_source
import settings
from jsonrpcserver.aio import methods

class Roulette777(object):
    def __init__(self):
        w3 = Web3(Web3.EthereumTesterProvider())
        self.eth = w3.eth
        self.roulette = self.contract()

    def contract(self):
        compiled_sol = compile_source(settings.contract_source_code,
                                      import_remappings=['=/', '-']
                                      )
        contract_interface = compiled_sol['<stdin>:Roulette777']
        self.eth.defaultAccount = self.eth.accounts[0]
        Roulette = self.eth.contract(abi=contract_interface['abi'],
                                 bytecode=contract_interface['bin']
                                 )
        tx_hash = Roulette.constructor().transact()
        tx_receipt = self.eth.waitForTransactionReceipt(tx_hash)
        roulette_data = self.eth.contract(address=tx_receipt.contractAddress,
                                      abi=contract_interface['abi']
                                      )
        return roulette_data

    def get_owner(self):
        owner = self.roulette.functions.getOwner().call()
        return owner

    def get_balance(self):
        balance = self.roulette.functions.getBalance().call()
        return balance

    def update_balance(self, amount):
        balance = self.roulette.functions.updateBalance(amount).call()
        tx_hash = self.roulette.functions.updateBalance(amount).transact()
        self.eth.waitForTransactionReceipt(tx_hash)
        return balance

    def bet_on_number(self, number, amount):
        tx_receipt = self.roulette.functions.betOnNumber(number, amount).call()
        tx_hash = self.roulette.functions.betOnNumber(number, amount).transact()
        self.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def _default_account(self):
        return self.eth.defaultAccount

    def accounts(self):
        return self.eth.accounts

    def client_get_balance(self, address=None):
        if address: address = self._default_account()
        return self.eth.getBalance(address)

    def get_bet(self, number):
        bet = list(self.roulette.functions.getBet(number).call())
        return bet

    def spin_wheel(self, address=None):
        if address: address = self.get_owner()
        # print(address)
        amount = self.roulette.functions.spinWheel(address).call()
        tx_hash = self.roulette.functions.spinWheel(address).transact()
        self.eth.waitForTransactionReceipt(tx_hash)
        return amount





#
# balance_1 = roulette.get_balance()
# print("Current balance: {}".format(balance_1))
# assert (roulette.get_owner() == roulette.accounts()[0])
# assert (balance_1 == 0)
#
# print("Returned balance: {}".format(balance_returned))
# balance_2 = roulette.get_balance()
# print("Current balance: {}".format(balance_2))
# assert (balance_2 == balance_1 + amount)
# amount_bet = 1000
# number_bet = 4
# bet_index = roulette.bet_on_number(number_bet, amount_bet)
# print("Bet index: {}".format(bet_index))
# assert (bet_index == 0)
# bet_1 = roulette.get_bet(bet_index)
# print("Bet 1: {}".format(bet_1))
# assert (bet_1[1] == 100)
# result = roulette.spin_wheel(roulette.get_owner())
# print("Result: {}".format(result))
