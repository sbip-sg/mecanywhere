from typing import Self
from web3 import Web3
import json


class PaymentContract:
    _contract_instance = None

    def __init__(self, abi_path, contract_address, url) -> None:
        self.w3 = Web3(Web3.HTTPProvider(url))
        self.tx_params = {
            "from": self.w3.eth.accounts[0],
            "gasPrice": self.w3.to_wei("50", "gwei"),
        }
        with open(abi_path) as abi_definition:
            self.abi = json.load(abi_definition)["abi"]

        self.contract = self.w3.eth.contract(address=contract_address, abi=self.abi)

    def __new__(cls, abi_path, contract_address, url) -> Self:
        if cls._contract_instance is None:
            cls._contract_instance = super().__new__(cls)
        return cls._contract_instance

    def get_due(self, did: str):
        return self.contract.functions.getDue(did).call()

    def set_due(self, nonce: int, did: str, source: str, amount: int):
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.setDue(
                nonce, did, source, amount
            ).transact(self.tx_params)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)

    def remove_due(self, nonce: int):
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.removeDue(nonce).transact(self.tx_params)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)

    def get_balance(self, did: str) -> int:
        return self.contract.functions.getBalance(did).call()

    def increase_balance(self, did: str, amount: int):
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.increaseBalance(did, amount).transact(
                self.tx_params
            )
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)

    def decrease_balance(self, did: str, amount: int):
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.decreaseBalance(did, amount).transact(
                self.tx_params
            )
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)
