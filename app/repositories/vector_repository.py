from app.infra.opensearch_client import get_opensearch_client
from app.core.config_loader import load_app_config
import uuid

# Load once (cached)
app_config = load_app_config()
OPENSEARCH_INDEX = app_config["opensearch"]["index"]
class VectorRepository:
    def __init__(self):
        self.client = get_opensearch_client()
        self.index = OPENSEARCH_INDEX

    def insert_chunk(self, text: str, embedding: list, metadata: dict):
        doc_id = str(uuid.uuid4())

        document = {
            "content": text,
            "embedding": embedding,
            **metadata,
        }

        self.client.index(
            index=self.index,
            body=document,
        )

        return doc_id
