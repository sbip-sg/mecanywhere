from web3 import Web3
import json
from abc import ABC, abstractmethod


class DiscoveryContract(ABC):
    @abstractmethod
    def set_ip_address_timestamp(self, ip_address, timestamp) -> None:
        pass

    @abstractmethod
    def getIpAddressTimestamp(self, ip_address) -> str:
        pass

    @abstractmethod
    def getAllIpAddressTimestamps(self):
        pass

    @abstractmethod
    def removeIpAddress(self, ip_address: str) -> None:
        pass


class EthDiscoveryContract(DiscoveryContract):
    def __init__(self, abi_path, contract_address, url, transaction_gas) -> None:
        self.w3 = Web3(Web3.HTTPProvider(url))
        self.transaction_gas = transaction_gas
        with open(abi_path) as abi_definition:
            self.abi = json.load(abi_definition)['abi']

        self.contract = self.w3.eth.contract(
            address=contract_address, abi=self.abi)

    def set_ip_address_timestamp(self, ip_address, timestamp) -> None:
        # Transaction parameters
        tx_params = {
            'from': self.w3.eth.accounts[0],
            'gas': self.transaction_gas,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        }

        # Sending the transaction to the network
        tx_hash = self.contract.functions.setIpAddressTimestamp(
            ip_address, timestamp).transact(tx_params)

        # Waiting for the transaction to be mined
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def getIpAddressTimestamp(self, ip_address) -> str:
        return self.contract.functions.getIpAddressTimestamp(ip_address).call()

    def getAllIpAddressTimestamps(self):
        ip_list, timestamp_list = self.contract.functions.getAllIpAddressTimestamps().call()
        return [(ip, timestamp) for (ip, timestamp) in zip(ip_list, timestamp_list)]

    def removeIpAddress(self, ip_address: str) -> None:
        tx_params = {
            'from': self.w3.eth.accounts[0],
            'gas': self.transaction_gas,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        }

        # Sending the transaction to the network
        tx_hash = self.contract.functions.removeIpAddress(
            ip_address).transact(tx_params)

        # Waiting for the transaction to be mined
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
