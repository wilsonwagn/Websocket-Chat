# Projeto WebSocket com FastAPI e Docker

Este projeto implementa uma aplicação de Chat com WebSocket utilizando FastAPI no Python, Docker-Compose, e Banco de Dados NoSQL com MongoDB.

## Instruções para Execução
1. Construir e iniciar os serviços Docker:
```bash
docker-compose up --build
```
2. Acessar/Testar a aplicação Websocket:
- Conecte-se ao WebSocket para enviar e receber mensagens, abra várias abas diferentes e envie mensagem simultaneamente:
```bash
http://localhost:8000/
```

## Dependências
As dependências do projeto estão listadas em `requirements.txt` e incluem:
- FastAPI
- Uvicorn
- Websockets
- Pymongo
- Entre outros
