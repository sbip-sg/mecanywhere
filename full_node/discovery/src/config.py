import json


class Config:
    def __init__(self, path: str) -> None:
        with open(path, 'r') as f:
            self.configuration = json.load(f)

    def get_contract_address(self) -> str:
        return self.configuration["contract"]["contract_address"]

    def get_abi_path(self) -> str:
        return self.configuration["contract"]["abi_path"]

    def get_contract_url(self) -> str:
        return self.configuration["contract"]["url"]

    def get_transaction_gas(self) -> int:
        return self.configuration["contract"]["transaction_gas"]
