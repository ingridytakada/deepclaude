from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
import json
import httpx
import os
from dotenv import load_dotenv
import traceback

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém as chaves de API do ambiente
ANTHROPIC_TOKEN = os.getenv("ANTHROPIC_API_TOKEN")
DEEPSEEK_TOKEN = os.getenv("DEEPSEEK_API_TOKEN")
HOST = "127.0.0.1"
PORT = 3000

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    try:
        data = await request.json()
        print("Dados recebidos:", data)
        
        headers = {
            "x-api-key": ANTHROPIC_TOKEN,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Ajustando o formato para a API da Anthropic
        api_data = {
            "model": "claude-3-opus-20240229",  # Modelo atualizado
            "messages": data.get("messages", []),
            "max_tokens": 1000,
            "stream": True
        }
        
        print("Enviando para API:", api_data)
        
        async def generate():
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=api_data,
                    timeout=30.0
                ) as response:
                    if response.status_code != 200:
                        error_content = await response.aread()
                        error_detail = error_content.decode()
                        print(f"Erro API: {error_detail}")
                        raise HTTPException(status_code=response.status_code, detail=error_detail)
                    
                    async for line in response.aiter_lines():
                        if line and line.strip():
                            yield f"{line}\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        print(f"Erro: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(f"Iniciando servidor em {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
