# Hybrid search
from app.infra.opensearch_client import get_opensearch_client
from app.infra.bedrock_embedding_client import EmbeddingBedrockClient
from app.core.config_loader import load_app_config, load_llm_config

# Load once (cached)
app_config = load_app_config()
llm_config = load_llm_config()

OPENSEARCH_INDEX = app_config["opensearch"]["index"]
RETRIEVAL_CFG = llm_config["retrieval"]


class SearchService:
    def __init__(self):
        self.os_client = get_opensearch_client()
        self.embed_client = EmbeddingBedrockClient()

    def hybrid_search(self, query: str, top_k: int | None = None):
        embedding = self.embed_client.embed_text(query)

        k = top_k or RETRIEVAL_CFG["top_k"]
        knn_k = RETRIEVAL_CFG.get("knn_k", k)
        bm25_boost = RETRIEVAL_CFG.get("bm25_boost", 2.0)

        body = {
            "size": k,
            "query": {
                "bool": {
                    "should": [
                        {
                            "knn": {
                                "embedding": {
                                    "vector": embedding,
                                    "k": knn_k,
                                }
                            }
                        },
                        {
                            "match": {
                                "content": {
                                    "query": query,
                                    "boost": bm25_boost,
                                }
                            }
                        }
                    ]
                }
            }
        }

        return self.os_client.search(
            index=OPENSEARCH_INDEX,
            body=body,
        )
