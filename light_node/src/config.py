import json


class Config:
    def __init__(self, path) -> None:
        with open(path, "r") as f:
            self.configuration = json.load(f)

    def get_heartbeat_url(self) -> str:
        return self.configuration["full_node_heartbeat"]

    def get_heartbeat_interval_sec(self) -> int:
        return self.configuration["heartbeat"]["interval"]

    def get_register_host_url(self) -> str:
        return self.configuration["full_node_register_host"]

    def get_deregister_host_url(self) -> str:
        return self.configuration["full_node_deregister_host"]
    
    def get_register_user_url(self) -> str:
        return self.configuration["full_node_register_user"]

    def get_deregister_user_url(self) -> str:
        return self.configuration["full_node_deregister_user"]

    def get_assign_host_url(self) -> str:
        return self.configuration["full_node_assign_host"]
    