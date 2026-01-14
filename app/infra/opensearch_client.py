import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from app.core.config import get_settings

from app.core.config_loader import load_app_config


app_config = load_app_config()
AWS_REGION = app_config["aws"]["region"]

def get_opensearch_client() -> OpenSearch:
    settings = get_settings()
    session = boto3.Session()
    credentials = session.get_credentials()

    if credentials is None:
        raise RuntimeError(
            "AWS credentials not found. "
            "Use `aws configure` locally or attach IAM Role in production."
        )

    frozen = credentials.get_frozen_credentials()

    awsauth = AWS4Auth(
        frozen.access_key,
        frozen.secret_key,
        AWS_REGION,
        "aoss",
        session_token=frozen.token,
    )

    return OpenSearch(
        hosts=[{"host": settings.OPENSEARCH_COLLECTION_ENDPOINT, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
