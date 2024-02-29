from web3 import Web3
import json

from config import Config



class Contract:
    def __init__(self, config: Config, abi_path: str, contract_address: str) -> None:
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.get_blockchain_provider_url()))
        with open(abi_path) as abi_definition:
            self.abi = json.load(abi_definition)["abi"]
        self.contract = self.w3.eth.contract(
            address=contract_address, abi=self.abi
        )

    def call_function(self, unbuilt_function, add_params = {}):
        try:
            print("Calling function: " + unbuilt_function.function_identifier)
            caller = self.config.get_wallet_address()

            built_function = unbuilt_function.build_transaction(
                {
                    "from": caller,
                    "gasPrice": self.w3.eth.gas_price,
                    **add_params,
                    "nonce": self.w3.eth.get_transaction_count(caller),
                    "chainId": self.w3.eth.chain_id,
                }
            )
            estimated_gas = self.w3.eth.estimate_gas(built_function) * 2
            built_function.update({"gas": estimated_gas})

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
