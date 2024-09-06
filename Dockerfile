# Use uma imagem base do Python
FROM python:3.11-slim

#Defina o diretório de trabalho dentro do conteiner
WORKDIR /app

COPY . .

#Instale as dependencias listadas do "requirements.txt"
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]