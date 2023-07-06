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

    def get_blockchain_provider_url(self) -> str:
        return self.configuration["contract"]["url"]
    
    def get_wallet_address(self) -> str:
        return self.configuration["wallet"]["address"]
    
    def get_wallet_private_key(self) -> str:
        return self.configuration["wallet"]["private_key"]

    def get_verify_vc_url(self) -> str:
        return self.configuration["did_verify_credential"]

    def get_redis_host(self) -> str:
        return self.configuration["redis"]["host"]

    def get_redis_port(self) -> int:
        return self.configuration["redis"]["port"]

    def get_access_token_key(self) -> str:
        return self.configuration["secrets"]["access_token_key"]

    def get_refresh_token_key(self) -> str:
        return self.configuration["secrets"]["refresh_token_key"]
