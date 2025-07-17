import asyncio
import os

import dotenv
from fastmcp import Client
from openai import OpenAI

caminho_servidor = 'http://localhost:8000/sse'
cliente_mcp = Client(caminho_servidor)


async def testar_servidor(cliente, busca):
    dotenv.load_dotenv()
    api_key = os.environ['CHAVE_API_OPENAI']
    async with cliente:
        resultado = await cliente.call_tool("buscar_wikipedia", arguments={'busca': busca})
        print(resultado)
        mensagem_sistema = f"""
        Você é um bot que faz buscas no wikipedia e sintetiza a resposta.
        O usuário buscou pelo seguinte tema: "{busca}".
        Para esta busca, você recebeu a seguinte resposta: "{resultado}".
        Com base nesse conteúdo, formate uma resposta amigável ao usuário.
        """
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=mensagem_sistema,
            input="Pode me falar mais sobre este assunto?",
        )
        print(response.output_text)


if __name__ == '__main__':
    busca = 'William Henry "Bill" Gates III'
    asyncio.run(testar_servidor(cliente=cliente_mcp, busca=busca))
