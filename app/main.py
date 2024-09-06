import json
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status)
from fastapi.responses import HTMLResponse
from typing import Annotated

import pymongo
from pymongo import MongoClient



app = FastAPI()

""" MongoDB — SQL: """

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
meu_banco = cliente['banco_de_dados']

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.clients = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
#
manager = ConnectionManager()     

#>>> Front-End:
@app.get("/")
async def get():
    with open("./testeChat.html", "r", encoding="utf-8") as f:
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
            #message_dateHour = json.loads(data)

            #Ao se conectar:
            if message_data["type"] == "name":
                manager.clients[client_id] = message_data["name"]
                await manager.broadcast(f"{message_data['name']} entrou no chat")

            # Ao enviar mensagens:
            elif message_data["type"] == "message":
                client_name = manager.clients.get(client_id, "Cliente desconhecido")
                timestamp = message_data.get("timestamp", "Sem hora") 
                await manager.broadcast(f"{timestamp} | {client_name} disse: {message_data['message']}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        client_name = manager.clients.get(client_id, "Cliente desconhecido")
        await manager.broadcast(f"Cliente: #{client_id} saiu do chat")