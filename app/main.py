import json
from fastapi import (FastAPI, WebSocket, WebSocketDisconnect)
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.websocket_manager import ConnectionManager
from app.database import save_clients

app = FastAPI()
manager = ConnectionManager()   
app.mount("/static", StaticFiles(directory="app/static"), name="static") #Montar a pasta estática com css e js
templates = Jinja2Templates(directory="app/templates")

#>>> Front-End:
@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("chatFront.html", {"request": request})

#>>> BackEnd/WebSocket:
@app.websocket("/ws/{client_id}")
async def websocket_endpoint2(websocket: WebSocket, client_id: int): 
    await manager.connect(websocket)
    await manager.send_personal_message(f"Seja bem vindo ao chat de Wilson, vamos começar os testes?", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data) #Lendo o JSON enviado do cliente!

            #Ao se conectar:
            if message_data["type"] == "name":

                manager.clients[client_id] = message_data["name"]
                save_clients(client_id, message_data["name"], message_data.get("timestamp", "Sem data/hora de acesso"))
                await manager.broadcast(f"{message_data['name']} entrou no chat")

            # Ao enviar mensagens:
            elif message_data["type"] == "message":

                client_name = manager.clients.get(client_id, "Cliente desconhecido")
                timestamp = message_data.get("timestamp", "Sem hora") 

                #Salvando o cliente no banco!
                await manager.broadcast(f"{timestamp} | {client_name} disse: {message_data['message']}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        client_name = manager.clients.get(client_id, "Cliente desconhecido")
        await manager.broadcast(f"Cliente: #{client_id} saiu do chat")