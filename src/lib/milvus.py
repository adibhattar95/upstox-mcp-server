from typing import List, Any, Tuple, Optional
from tqdm import tqdm
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

from src.utils.constants import MILVUS_HOST, MILVUS_PORT

index_params = {
    "metric_type":"COSINE",
    "index_type":"HNSW",
    "params": {"M": 64, "efConstruction":200}
}

search_params = {
    "metric_type":"COSINE",
    "params": {"ef":200}
}

class MilvusClient:
    def __init__(self, collection_name: str, model_name: str = 'all-MiniLM-L6-v2', equity_dict: Optional[Path] = None,
                  batch_size: int = 100, field_to_embed: str | None = None):
        self.model = SentenceTransformer(model_name)
        self.collection = collection_name
        if equity_dict is not None:
            with open(equity_dict, 'r') as json_file:
                self.equity_dict = json.load(json_file)
        self.batch_size = batch_size
        self.field_to_embed = field_to_embed
        connections.connect(alias='default', host = MILVUS_HOST, port = MILVUS_PORT)

    def _batch_encode(self) -> List[Any]:
        embeddings = []
        for i in tqdm(range(0, len(self.equity_dict), self.batch_size)):
            batch_texts = [record[self.field_to_embed] for record in self.equity_dict[i:i + self.batch_size]]
            encoded_batch = self.model.encode(batch_texts, normalize_embeddings=True)
            embeddings.extend(encoded_batch)
        return embeddings
    
    def create_collection(self):
        collections = utility.list_collections()
        if self.collection in collections:
            utility.drop_collection(collection_name=self.collection)
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="short_name", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="instrument_key", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name='name_embedding', dtype=DataType.FLOAT_VECTOR, dim=self.model.get_sentence_embedding_dimension())
        ]
        schema = CollectionSchema(fields, description="Collection for saving Instrument Keys for Equity Stocks")
        collection = Collection(name=self.collection, schema=schema)
        embeddings = self._batch_encode()
        names = [stock.get('name', 'NA') for stock in self.equity_dict]
        short_names = [stock.get('short_name', 'NA') for stock in self.equity_dict]
        instrument_keys = [stock.get('instrument_key', 'NA') for stock in self.equity_dict]
        insert_data = [names, short_names, instrument_keys, embeddings]
        collection.insert(insert_data)
        collection.flush()
        print("Collection Created")

    def create_index(self):
        collection = Collection(self.collection)
        collection.create_index(field_name='name_embedding', index_params=index_params)
        print("Index Created")
    
    def run_equity_search(self, search_name: str) -> Tuple[str | None, str | None]:
        collection = Collection(self.collection)
        collection.load()
        search_embedding = self.model.encode(search_name, normalize_embeddings=True)
        search_results = collection.search(
            data=[search_embedding],
            anns_field="name_embedding",
            param=search_params,
            limit=1,
            output_fields=['name', 'instrument_key']
        )
        name = None
        instrument_key=None
        for hits in search_results: # type: ignore
            for hit in hits:
                name = hit.get('name')
                instrument_key = hit.get('instrument_key')
        return name, instrument_key

