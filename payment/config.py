import json
from pydantic import BaseSettings
import os


class Config:
    class SecretSettings(BaseSettings):
        wallet_address: str = None
        wallet_private_key: str = None
        access_token_key: str = None
        refresh_token_key: str = None

        class Config:
            env_file = ".env"

    def __init__(self, *paths: str) -> None:
        self.configuration = {}
        self.secrets = Config.SecretSettings()
        _environment = ""

        # Populate configuration from json files
        for path in paths:
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                    if config["environment"]:
                        _environment = config["environment"]
                        config = config[_environment]
                    self.configuration.update(config)
            except:
                pass

        # Try overwriting from docker secrets
        try:
            for dirpath, dirnames, files in os.walk("/run/secrets"):
                for file_name in files:
                    try:
                        secret = open(os.path.join(dirpath, file_name), "r").read().strip()
                        setattr(self.secrets, file_name, secret)
                    except:
                        pass
        except:
            pass

    def get_access_token_key(self) -> str:
        return self.secrets.access_token_key

    def get_refresh_token_key(self) -> str:
        return self.secrets.refresh_token_key

    def get_contract_address(self) -> str:
        return self.configuration["contract"]["contract_address"]

    def get_abi_path(self) -> str:
        return self.configuration["contract"]["abi_path"]

    def get_blockchain_provider_url(self) -> str:
        return self.configuration["contract"]["url"]

    def get_wallet_address(self) -> str:
        return self.secrets.wallet_address

    def get_wallet_private_key(self) -> str:
        return self.secrets.wallet_private_key

    def get_verify_vc_url(self) -> str:
        return self.configuration["verify_vc_url"]

    def get_redis_host(self) -> str:
        return self.configuration["redis"]["host"]

    def get_redis_port(self) -> str:
        return self.configuration["redis"]["port"]
