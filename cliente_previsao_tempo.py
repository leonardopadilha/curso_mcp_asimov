import asyncio
import os

import dotenv
from fastmcp import Client
from openai import OpenAI

caminho_servidor = 'http://localhost:8000/sse'
cliente_mcp = Client(caminho_servidor)


async def testar_servidor(cliente, local):
    dotenv.load_dotenv()
    api_key = os.environ['CHAVE_API_OPENAI']
    async with cliente:
      argumentos={'local': local}
      
      # Os argumentos são os mesmos devido a forma como as duas funções foram criadas
      tempo_atual = await cliente.call_tool("buscar_tempo_atual", arguments=argumentos)
      previsao_tempo = await cliente.call_tool("buscar_previsao_tempo", arguments=argumentos)

      mensagem_sistema = f"""
      Você é um bot que faz buscas de previsão do tempo e sintetiza a resposta.
      O usuário buscou pela previsão do seguinte local: "{local}".
      Para esta busca, você recebeu a seguinte previsão: "{previsao_tempo}".
      Além disso, o tempo atual é: "{tempo_atual}".
      Com base nesse conteúdo, formate uma resposta amigável ao usuário.
      """
      client = OpenAI(api_key=api_key)
      response = client.responses.create(
          model="gpt-4o-mini",
          instructions=mensagem_sistema,
          input="Qual é a previsão do tempo no local indicado?",
      )
      print(response.output_text)


if __name__ == '__main__':
    local = input("Informe um local para busca: ")
    asyncio.run(testar_servidor(
      cliente=cliente_mcp, 
      local=local)
    )
