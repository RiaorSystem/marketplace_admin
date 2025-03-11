from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

#Storing active WebSocket Connections
active_connections: Dict[int, WebSocket] = {}

@app.websocket("ws/chat/{user_id}")
async def chat_websocket(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            data =  await websocket.receive_text()
            receiver_id, message = data.split("|", 1)

            if int(receiver_id) in active_connections:
                await active_connections[int(receiver_id)].send_text(f"{user_id}: {message}")

    except WebSocketDisconnect:
        del active_connections[user_id]