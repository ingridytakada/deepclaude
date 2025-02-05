import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

async def stream_response():
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                "http://127.0.0.1:3000/",
                headers={
                    "Content-Type": "application/json",
                    "X-DeepSeek-API-Token": os.getenv("DEEPSEEK_API_TOKEN"),
                    "X-Anthropic-API-Token": os.getenv("ANTHROPIC_API_TOKEN")
                },
                json={
                    "model": "claude-3-opus-20240229",
                    "messages": [
                        {
                            "role": "user",
                            "content": "Me conte uma curiosidade interessante sobre o Japão"
                        }
                    ]
                }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            json_str = line[6:]  # Remove o prefixo "data: "
                            data = json.loads(json_str)
                            if data["type"] == "content_block_delta":
                                text = data["delta"].get("text", "")
                                # Imprime apenas o texto, sem mensagens de debug
                                print(text, end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                        except KeyError:
                            pass

        except Exception as e:
            print(f"Erro: {str(e)}")

if __name__ == "__main__":
    asyncio.run(stream_response())
