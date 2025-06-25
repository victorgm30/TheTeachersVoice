from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

connections = []

@app.get("/")
async def root():
    return HTMLResponse("<h3>Bem-vindo ao Voz na Sala! Acesse /professora ou /aluno</h3>")

@app.get("/professora")
async def professora():
    return HTMLResponse(open("static/professora.html").read())

@app.get("/aluno")
async def aluno():
    return HTMLResponse(open("static/aluno.html").read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections:
                if conn != websocket:
                    await conn.send_text(data)
    except:
        connections.remove(websocket)
