from decimal import Decimal
from typing import Self
from config import Config
from web3 import Web3
import json


# Shared contract with payment service
class PaymentContract:
    _contract_instance = None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.get_blockchain_provider_url()))
        with open(config.get_abi_path()) as abi_definition:
            self.abi = json.load(abi_definition)["abi"]
        self.contract = self.w3.eth.contract(
            address=config.get_contract_address(), abi=self.abi
        )

    def __new__(cls, config) -> Self:
        if cls._contract_instance is None:
            cls._contract_instance = super().__new__(cls)
        return cls._contract_instance

    def call_function(self, unbuilt_function, add_params):
        try:
            print("Calling function: " + unbuilt_function.function_identifier)
            caller = self.config.get_wallet_address()
            built_function = unbuilt_function.build_transaction(
                {
                    "from": caller,
                    "gasPrice": self.w3.to_wei("50", "gwei"),
                    **add_params,
                    "nonce": self.w3.eth.get_transaction_count(caller),
                    "chainId": self.w3.eth.chain_id,
                }
            )
            signed_tx = self.w3.eth.account.sign_transaction(
                built_function, self.config.get_wallet_private_key()
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt["status"] != 1:
                raise Exception(
                    "Transaction failed. Check etherscan for "
                    + tx_receipt.transactionHash.hex()
                )
        except ValueError as e:
            raise Exception(e)

    # function not used in this service
    # # amount is in ether
    # def withdraw(self, did: str, address: str, amount: int):
    #     wei_amount = self.w3.to_wei(Decimal(amount), "ether")
    #     unbuilt_function = self.contract.functions.withdraw(did, address, wei_amount)
    #     self.call_function(unbuilt_function, {"gas": 300000})

    def get_balance(self, did: str) -> int:
        balance = self.contract.functions.getBalance(did).call()
        return self.w3.from_wei(balance, "ether")

    # amount is in ether
    def increase_balance(self, did: str, amount: int):
        print("Increasing balance of", did, "by", amount)
        if amount <= 0:
            return
        wei_amount = self.w3.to_wei(Decimal(amount), "ether")
        unbuilt_function = self.contract.functions.increaseBalance(did, wei_amount)
        self.call_function(unbuilt_function, {"gas": 300000})
        print("Increased balance of", did, "by", amount)

    # amount is in ether
    def decrease_balance(self, did: str, amount: int):
        print("Decreasing balance of", did, "by", amount)
        if amount <= 0:
            return
        wei_amount = self.w3.to_wei(Decimal(amount), "ether")
        unbuilt_function = self.contract.functions.decreaseBalance(did, wei_amount)
        self.call_function(unbuilt_function, {"gas": 300000})
        print("Decreased balance of", did, "by", amount)
