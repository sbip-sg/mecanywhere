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
