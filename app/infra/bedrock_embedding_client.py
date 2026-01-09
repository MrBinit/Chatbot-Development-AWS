import json
import boto3
from app.core.config import settings

class EmbeddingBedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.AWS_REGION,
        )

    def embed_text(self, text: str) -> list[float]:
        response = self.client.invoke_model(
            modelId=settings.EMBEDDING_MODEL_ID,
            body=json.dumps({"inputText": text}),
            accept="application/json",
            contentType="application/json",
        )

        body = json.loads(response["body"].read())

        if "embedding" not in body:
            raise RuntimeError(
                f"Embedding missing in Bedrock response: {body}"
            )

        return body["embedding"]

