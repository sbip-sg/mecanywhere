import json
import os

from pydantic_settings import BaseSettings


class Config:
    class SecretSettings(BaseSettings):
        tower_private_key: str = None

        class Config:
            env_file = os.path.join(os.path.dirname(__file__), '.env')

    def __init__(self, *paths: str) -> None:
        self.configuration = {}
        self.secrets = Config.SecretSettings()
        _environment = ""

        # Populate configuration from json files
        for path in paths:
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                    if "environment" in config and config["environment"]:
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

    def get_blockchain_provider_url(self) -> str:
        return self.configuration["blockchain"]["url"]

    def get_tower_private_key(self) -> str:
        return self.secrets.tower_private_key
