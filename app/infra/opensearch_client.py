import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from app.core.config import settings

def get_opensearch_client() -> OpenSearch:
    session = boto3.Session()
    credentials = session.get_credentials()
    region = settings.AWS_REGION

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        "aoss",
        session_token=credentials.token,
    )

    client = OpenSearch(
        hosts=[{"host": settings.OPENSEARCH_COLLECTION_ENDPOINT, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )

    return client
