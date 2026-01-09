from app.infra.opensearch_client import get_opensearch_client
from app.infra.bedrock_embedding_client import EmbeddingBedrockClient

OPENSEARCH_INDEX = "rag-index"

def main():
    os_client = get_opensearch_client()
    embed_client = EmbeddingBedrockClient()

    query = "What are the key objectives of the National AI Policy?"

    # Generate embedding
    embedding = embed_client.embed_text(query)
    print("Embedding dim:", len(embedding))

    # Semantic search
    response = os_client.search(
        index=OPENSEARCH_INDEX,
        body={
            "size": 5,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": 5
                    }
                }
            }
        }
    )

    #Print results
    for i, hit in enumerate(response["hits"]["hits"], 1):
        print("\n" + "=" * 60)
        print(f"Result #{i} | score={hit['_score']}")
        print(hit["_source"]["content"][:400])

if __name__ == "__main__":
    main()
