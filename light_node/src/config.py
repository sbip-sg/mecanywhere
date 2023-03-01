import json


class Config:
    def __init__(self, path) -> None:
        with open(path, 'r') as f:
            self.configuration = json.load(f)

    def get_heartbeat_url(self) -> str:
        return self.configuration['heartbeat']['url']

    def get_heartbeat_interval_sec(self) -> int:
        return self.configuration['heartbeat']['interval']
