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

    def get_cleanup_interval(self) -> int:
        return self.configuration["cleanup"]["interval_in_sec"]

    def get_cleanup_expire(self) -> int:
        return self.configuration["cleanup"]["expire_in_sec"]

    def get_did_service_url(self) -> str:
        return self.configuration["did"]["url"]
    
    def get_did_service_verify_credential_url(self) -> str:
        return self.get_did_service_url() + "/api/v1/credential/verify"