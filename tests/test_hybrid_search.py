from app.services.retrieval_service import SearchService

def main():
    service = SearchService()

    query = "AI governance and ethical framework in Nepal"

    response = service.hybrid_search(query, top_k=5)

    for i, hit in enumerate(response["hits"]["hits"], 1):
        print("\n" + "=" * 60)
        print(f"Rank {i} | score={hit['_score']}")
        print(hit["_source"]["content"][:400])

if __name__ == "__main__":
    main()
