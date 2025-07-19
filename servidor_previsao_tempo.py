import os
import dotenv
import requests
from fastmcp import FastMCP

servidor_mcp = FastMCP('mcp-previsao-tempo')

@servidor_mcp.tool()
def buscar_tempo_atual(local: str)-> dict:
  dotenv.load_dotenv()
  app_id = os.environ['CHAVE_API_OPENWEATHER']
  url = f'https://api.openweathermap.org/data/2.5/weather'
  params = {
    'q': local,
    'appid': app_id,
    'units': 'metric',
    'lang': 'pt_br'
  }
  response = requests.get(url=url, params=params)
  return response.json()

@servidor_mcp.tool()
def buscar_previsao_tempo(local: str)-> dict:
  dotenv.load_dotenv()
  app_id = os.environ['CHAVE_API_OPENWEATHER']
  url = f'https://api.openweathermap.org/data/2.5/forecast'
  params = {
    'q': local,
    'appid': app_id,
    'units': 'metric',
    'lang': 'pt_br'
  }
  response = requests.get(url=url, params=params)
  return response.json()

if __name__ == "__main__":
  servidor_mcp.run(transport='stdio')
