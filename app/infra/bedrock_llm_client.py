import asyncio
import logging
import boto3
from app.core.config_loader import load_app_config, load_llm_config
from app.core.error import api_error

logger = logging.getLogger(__name__)

# Load configs ONCE (cached via lru_cache)
app_config = load_app_config()
llm_config = load_llm_config()

AWS_REGION = app_config["aws"]["region"]
LLM_MODEL_ID = llm_config["llm"]["model_id"]
GENERATION_CFG = llm_config["llm"]["generation"]

# Bedrock client (infra-level)
brt = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)

async def generate_completion(prompt: str) -> str:
    """
    Low-level LLM call.
    Does NOT know about RAG, retrieval, or OpenSearch.
    """
    loop = asyncio.get_running_loop()

    try:
        response = await loop.run_in_executor(
            None,
            lambda: brt.converse(
                modelId=LLM_MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": GENERATION_CFG["max_tokens"],
                    "temperature": GENERATION_CFG["temperature"],
                    "topP": GENERATION_CFG["top_p"],
                },
            )
        )

        return response["output"]["message"]["content"][0]["text"]

    except Exception:
        logger.exception("Bedrock inference failed")
        api_error(
            status_code=500,
            code="BEDROCK_INFERENCE_FAILED",
            message="Failed to generate response from model",
        )
