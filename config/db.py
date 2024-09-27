from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path
import certifi

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
conn = MongoClient(os.getenv('ATLAS_URI'), tlsCAFile=certifi.where() )