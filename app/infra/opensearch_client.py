import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from app.core.config import settings
from app.core.config_loader import load_app_config

# YAML (behavior / infra config)
app_config = load_app_config()
AWS_REGION = app_config["aws"]["region"]

# ENV (endpoint)
OPENSEARCH_ENDPOINT = settings.OPENSEARCH_COLLECTION_ENDPOINT


def get_opensearch_client() -> OpenSearch:
    session = boto3.Session()
    credentials = session.get_credentials()

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        AWS_REGION,
        "aoss",
        session_token=credentials.token,
    )

    return OpenSearch(
        hosts=[{"host": OPENSEARCH_ENDPOINT, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
