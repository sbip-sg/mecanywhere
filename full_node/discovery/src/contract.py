from typing import Self, List, Tuple
from web3 import Web3
import json
from abc import ABC, abstractmethod


class DiscoveryContract(ABC):
    @abstractmethod
    def set_user(self, did: str, timestamp: int, latency: int) -> None:
        pass

    @abstractmethod
    def get_user_queue(self, current_timestamp: int) -> str:
        pass

    @abstractmethod
    def get_all_did_to_timestamps(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def remove_user(self, did: str) -> None:
        pass

    @abstractmethod
    def remove_users(self, dids: List[str]) -> None:
        pass


class EthDiscoveryContract(DiscoveryContract):
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

    # record user in the contract
    def set_user(self, did: str, timestamp: int, latency: int) -> None:
        try:
            self.tx_params["gas"] = 400000
            # Sending the transaction to the network
            tx_hash = self.contract.functions.setUser(did, timestamp, latency).transact(
                self.tx_params
            )

            # Waiting for the transaction to be mined
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)

    # get arbitrary queue name from the contract
    def get_user_queue(self, current_timestamp: int) -> str:
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.lazyRemoveExpiredUsers(
                current_timestamp
            ).transact(self.tx_params)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return self.contract.functions.getFirstUserQueue().call()
        except ValueError as e:
            print(e)

    # get all dids and timestamps from the contract
    def get_all_did_to_timestamps(self) -> List[Tuple[str, int]]:
        try:
            (
                user_list,
                timestamp_list,
            ) = self.contract.functions.getAllDidToTimestamps().call()
            return [
                (did, timestamp) for (did, timestamp) in zip(user_list, timestamp_list)
            ]
        except ValueError as e:
            print(e)

    # remove user from the contract
    def remove_user(self, did: str) -> None:
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.removeUser(did).transact(self.tx_params)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)

    # remove users from the contract
    def remove_users(self, dids: List[str]) -> None:
        try:
            self.tx_params["gas"] = 300000
            tx_hash = self.contract.functions.removeUsers(dids).transact(self.tx_params)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except ValueError as e:
            print(e)
