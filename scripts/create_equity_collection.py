import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lib.milvus import MilvusClient
from src.utils.constants import COLLECTION_NAME

script_path = Path(__file__).resolve()
data_path = script_path.parent.parent / 'data' / 'equity_keys.json'

print("🛠️ Creating Vector DB!")
vector_db_creator = MilvusClient(COLLECTION_NAME, 'all-MiniLM-L6-v2', data_path, 100, 'name')
vector_db_creator.create_collection()
vector_db_creator.create_index()