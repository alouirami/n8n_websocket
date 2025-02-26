import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# WebSocket route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            name = await websocket.recv_text()
            print(f"Server Received (WebSocket): {name}")
            greeting = f"Hello {name}!"
            await websocket.send_text(greeting)
            print(f"Server Sent (WebSocket): {greeting}")
    except WebSocketDisconnect:
        print("Client disconnected")

# HTTP route
@app.get("/")
async def get_root():
    html_content = """
    <html>
        <head><title>FastAPI WebSocket Example</title></head>
        <body>
            <h1>Welcome to FastAPI WebSocket Server!</h1>
            <p>Use WebSocket at <code>/ws</code> endpoint for WebSocket communication.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/greet")
async def greet(name: str = "World"):
    greeting = f"Hello {name}!"
    print(f"Server Received (HTTP): {name}")
    return {"message": greeting}