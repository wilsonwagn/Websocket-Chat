import json
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect)
from fastapi.responses import HTMLResponse
from app.websocket_manager import ConnectionManager
from app.database import save_clients

app = FastAPI()
manager = ConnectionManager()   

#>>> Front-End:
@app.get("/")
async def get():
    with open("./chatFront.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

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