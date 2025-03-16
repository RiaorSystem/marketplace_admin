import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List

app = FastAPI()

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track connected clients
active_connections: Dict[int, List[WebSocket]] = {}

@app.post("/track_order/{order_id}")
async def update_order_status(order_id: int, data: Dict):
    """Receive order status update from Django and notify clients"""
    logger.info(f"Received POST notification for order {order_id}: {data}")
    status = data.get("status")
    if not status:
        raise HTTPException(status_code=400, detail="Status missing")
    await notify_clients(order_id, status)
    return {"message": "Order status updated"}

@app.websocket("/track_order/{order_id}")
async def track_order(websocket: WebSocket, order_id: int):
    """WebSocket connection for order tracking"""
    await websocket.accept()
    logger.info(f"✅ WebSocket connected: Order {order_id}")

    # Send initial confirmation to client
    await websocket.send_json({"message": "Connected", "order_id": order_id})

    if order_id not in active_connections:
        active_connections[order_id] = []
    
    active_connections[order_id].append(websocket)

    try:
        # Keep connection open without expecting client messages
        while True:
            await websocket.receive()  # Non-blocking keep-alive
    except WebSocketDisconnect:
        active_connections[order_id].remove(websocket)
        if not active_connections[order_id]:
            del active_connections[order_id]
        logger.info(f"❌ WebSocket disconnected: Order {order_id}")
    except Exception as e:
        logger.error(f"❌ WebSocket error for Order {order_id}: {e}")
        active_connections[order_id].remove(websocket)
        if not active_connections[order_id]:
            del active_connections[order_id]

async def notify_clients(order_id: int, status: str):
    """Send real-time updates to all clients tracking an order"""
    if order_id in active_connections:
        for connection in active_connections[order_id]:
            try:
                await connection.send_json({"order_id": order_id, "status": status})
                logger.info(f"📡 WebSocket Update Sent: Order {order_id} -> {status}")
            except Exception as e:
                logger.error(f"❌ Failed to send WebSocket update: {e}")
                active_connections[order_id].remove(connection)