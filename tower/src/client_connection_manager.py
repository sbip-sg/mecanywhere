from fastapi import WebSocket

class ClientConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, tuple[str, WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        task_id: str,
        host_address: str
    ) -> bool:
        # await websocket.accept()
        if task_id in self.active_connections:
            websocket.disconnect()
            return False
        else:
            self.active_connections[task_id] = (host_address, websocket)
            return True

    def disconnect(self, task_id: str):
        del self.active_connections[task_id]

    async def send_output(
        self,
        task_id: str,
        host_address: str,
        output_bytes: bytes
    ) -> bool:
        if task_id in self.active_connections:
            if self.active_connections[task_id][0] == host_address:
                await self.active_connections[
                    task_id][1].send_bytes(output_bytes)
                # self.active_connections[task_id][1].disconnect()
                self.disconnect(task_id=task_id)
                return True
        return False
