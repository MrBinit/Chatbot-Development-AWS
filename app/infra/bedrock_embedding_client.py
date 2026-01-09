import json
import boto3

from app.core.config_loader import load_app_config

# Load once (cached via lru_cache)
app_config = load_app_config()

AWS_REGION = app_config["aws"]["region"]
EMBEDDING_MODEL_ID = app_config["embedding"]["model_id"]


class EmbeddingBedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )

    def embed_text(self, text: str) -> list[float]:
        response = self.client.invoke_model(
            modelId=EMBEDDING_MODEL_ID,
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
