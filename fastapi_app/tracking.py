from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "FastAPI is running"}

@app.websocket("/track_order/{order_id}")
async def track_order(websocket: WebSocket, order_id: int):
    """WebSocket connection for order tracking"""
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        pass  # Handle disconnection
