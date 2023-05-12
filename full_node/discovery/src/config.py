import json


class Config:
    def __init__(self, *paths: str) -> None:
        self.configuration = {}
        for path in paths:
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                    self.configuration.update(config)
            except:
                pass

    def get_contract_address(self) -> str:
        return self.configuration["contract"]["contract_address"]

    def get_abi_path(self) -> str:
        return self.configuration["contract"]["abi_path"]

    def get_contract_url(self) -> str:
        return self.configuration["contract"]["url"]

    def get_transaction_gas(self) -> int:
        return self.configuration["contract"]["transaction_gas"]

    def get_verify_vc_url(self) -> str:
        return self.configuration["did_verify_credential"]