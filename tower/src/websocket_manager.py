from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.connected_clients = {}
    
    async def accept(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.connected_clients[client_id] = websocket
        print(f"Client {client_id} just connected")
    
    def disconnect(self, client_id: str):
        if client_id in self.connected_clients:
            del self.connected_clients[client_id]

    async def send_message(self, client_id: str, data: str):
        if client_id in self.connected_clients:
            target_conn = self.connected_clients[client_id]
            await target_conn.send_text(data)
            print(f"Message sent to client {client_id}")
            return True
        else:
            raise ValueError("Client not found")
        
    async def receive_message(self, client_id: str):
        if client_id in self.connected_clients:
            target_conn = self.connected_clients[client_id]
            res = await target_conn.receive_text()
            print(f"Response received from client {client_id}")
            return res
        else:
            raise ValueError("Client not found")
        