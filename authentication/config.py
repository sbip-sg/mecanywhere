import json
import os

from pydantic import BaseSettings


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

        # Populate configuration from json files
        for path in paths:
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                    self.configuration.update(config)
            except:
                pass

        # Populate configuration from docker secrets
        if not os.environ.get("docker_testnet"):
            pass
        for dirpath, dirnames, files in os.walk("/run/secrets"):
            for file_name in files:
                try:
                    secret = open(os.path.join(dirpath, file_name), "r").read().strip()
                    setattr(self.secrets, file_name, secret)
                except:
                    pass

    def get_db_url(self) -> str:
        return self.configuration["db_url"]
    
    def get_issuer_url(self) -> str:
        return self.configuration["issuer_url"]
    
    def get_create_credential_url(self) -> str:
        return self.get_issuer_url() + self.configuration["create_credential_route"]
    
    def get_create_schema_url(self) -> str:
        return self.get_issuer_url() + self.configuration["create_schema_route"]
    
    def get_issuer_did(self) -> str:
        return self.configuration["issuer_did"]
    
    def get_cpt_id(self) -> int:
        return self.configuration["cpt_id"]
