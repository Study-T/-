from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["websocket"])

ACTIVE_CONNECTIONS: dict[int, set[WebSocket]] = {}


@router.websocket("/task/{task_id}")
async def task_progress(ws: WebSocket, task_id: int):
    await ws.accept()
    ACTIVE_CONNECTIONS.setdefault(task_id, set()).add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ACTIVE_CONNECTIONS[task_id].discard(ws)
        if not ACTIVE_CONNECTIONS[task_id]:
            del ACTIVE_CONNECTIONS[task_id]


async def notify_task_progress(task_id: int, data: dict):
    connections = ACTIVE_CONNECTIONS.get(task_id, set())
    for ws in list(connections):
        try:
            await ws.send_json(data)
        except Exception:
            connections.discard(ws)
