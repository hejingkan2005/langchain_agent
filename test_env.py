import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
print(f'Env file exists: {env_path.exists()}')
print(f'Env path: {env_path}')
load_dotenv(dotenv_path=env_path)
print(f'LLM_Model: {os.getenv("LLM_Model")}')
print(f'LLM_Base_URL: {os.getenv("LLM_Base_URL")}')
print(f'WEATHER_API_KEY: {os.getenv("WEATHER_API_KEY")}')
