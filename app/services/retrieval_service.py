# Hybrid search 
from app.infra.opensearch_client import get_opensearch_client
from app.infra.bedrock_embedding_client import EmbeddingBedrockClient
from app.core.config import settings

class SearchService:
    def __init__(self):
        self.os_client = get_opensearch_client()
        self.embed_client = EmbeddingBedrockClient()

    def hybrid_search(self, query: str, top_k: int = 5):
        embedding = self.embed_client.embed_text(query)

        body = {
            "size": top_k,
            "query": {
                "bool": {
                    "should": [
                        {
                            "knn": {
                                "embedding": {
                                    "vector": embedding,
                                    "k": top_k
                                }
                            }
                        },
                        {
                            "match": {
                                "content": {
                                    "query": query,
                                    "boost": 2.0
                                }
                            }
                        }
                    ]
                }
            }
        }

        return self.os_client.search(
            index=settings.OPENSEARCH_INDEX,
            body=body
        )
