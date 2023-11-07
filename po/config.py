import json
import os

from pydantic import BaseSettings


class Config:
    class SecretSettings(BaseSettings):

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

    def get_db_url(self) -> str:
        return self.configuration["db_url"]

    def get_issuer_url(self) -> str:
        return self.configuration["issuer_url"]
    
    def get_verifier_url(self) -> str:
        return self.configuration["verifier_url"]

    def get_create_credential_url(self) -> str:
        return self.get_issuer_url() + self.configuration["create_credential_route"]

    def get_create_schema_url(self) -> str:
        return self.get_issuer_url() + self.configuration["create_schema_route"]

    def get_issuer_did(self) -> str:
        return self.configuration["issuer_did"]

    def get_cpt_id(self) -> int:
        return self.configuration["cpt_id"]
