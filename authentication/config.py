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
