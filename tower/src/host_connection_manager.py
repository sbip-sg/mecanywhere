from fastapi import WebSocket

class HostConnectionManager:
    def __init__(self):
        # host_address: WebSocket
        self.active_connections: dict[str,  WebSocket] = {}

    async def connect(
        self,
        websocket: WebSocket,
        host_address: str
    ) -> bool:
        # await websocket.accept()
        if host_address in self.active_connections:
            # websocket.disconnect()
            # websocket.close() ? maybe
            return False
        else:
            self.active_connections[host_address] = websocket
            return True

    def disconnect(self, host_address: str):
        del self.active_connections[host_address]

    async def send_input(
        self,
        host_address: str,
        input_bytes: bytes
    ) -> bool:
        if host_address in self.active_connections:
            await self.active_connections[
                host_address].send_bytes(input_bytes)
            return True
        return False
