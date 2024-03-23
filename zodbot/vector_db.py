from pymilvus import (
    MilvusClient,
    DataType
)
from pymilvus import model
import numpy as np
import pandas as pd

class VectorDB:
    def __init__(self, endpoint, token):
        self.db_name = "test_db"
        self.client = MilvusClient(
            uri=endpoint,
            token=token 
        )

        if not self.client.has_collection("messages"):
            self._create_message_collection()

    def _create_message_collection(self):
        schema = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )

        # 3.2. Add fields to schema
        schema.add_field(field_name="uid", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="messages", datatype=DataType.FLOAT_VECTOR, dim=384)

        # 3.3. Prepare index parameters
        index_params = self.client.prepare_index_params()

        # 3.4. Add indexes
        index_params.add_index(
            field_name="uid"
        )

        index_params.add_index(
            field_name="messages", 
            index_type="AUTOINDEX",
            metric_type="IP"
        )

        # 3.5. Create a collection
        self.client.create_collection(
            collection_name="messages",
            schema=schema,
            index_params=index_params
        )

    def insert(self, uid, message):
        # Convert message using pandas
        sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
            model_name='all-MiniLM-L6-v2', # Specify the model name
            device='cpu' # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        )
        vectors = sentence_transformer_ef.encode_documents([
            message
        ])

        self.client.insert(
            collection_name="messages",
            data=[
                {"uid": uid, "messages": vectors[0]}
            ]
        )

    def search(self, message, top_k):
        # Convert message using pandas
        sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
            model_name='all-MiniLM-L6-v2', # Specify the model name
            device='cpu' # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        )
        vectors = sentence_transformer_ef.encode_documents([
            message
        ])

        return self.client.search(
            collection_name="messages",
            data=vectors,
            top_k=top_k
        )
    
    def reset_database(self):
        self.client.drop_collection("messages")
        self._create_message_collection()

    def close(self):
        self.client.close()


vector_db = VectorDB("http://localhost:19530", "minioadmin")