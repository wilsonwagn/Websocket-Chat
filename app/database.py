import pymongo
db = pymongo.MongoClient("mongodb://mongodb:27017") #Banco de dados
collection = db.get_database("chat_DB").get_collection("clients")

def save_clients(client_id, client_name, connected_at):
    client = {
        "client_id": client_id,
        "client_name": client_name,
        "connected_at": connected_at}
    result = collection.insert_one(client)
    print(f">>> Cliente ({client_name}) salvo com sucesso! ID Inserido: {result}")
