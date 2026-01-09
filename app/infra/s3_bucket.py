import boto3
import os
from botocore.exceptions import ClientError
from app.core.logger import get_logger

logger = get_logger(__name__)


class S3Storage:
    def __init__(self, bucket_name: str, region: str):
        self.bucket_name = bucket_name
        self.region = region

        # IMPORTANT: bind the region explicitly
        self.s3 = boto3.resource("s3", region_name=region)
        self.s3_client = boto3.client("s3", region_name=region)

        self.bucket = self.s3.Bucket(bucket_name)

    def ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info("S3 bucket '%s' already exists", self.bucket_name)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "404":
                logger.info(
                    "Creating S3 bucket '%s' in region %s",
                    self.bucket_name,
                    self.region,
                )
                if self.region == "us-east-1":
                    self.bucket.create()
                else:
                    self.bucket.create(
                        CreateBucketConfiguration={
                            "LocationConstraint": self.region
                        }
                    )

                self.bucket.wait_until_exists()
                logger.info("S3 bucket '%s' created successfully", self.bucket_name)

            else:
                logger.error(
                    "Failed to access bucket '%s': %s",
                    self.bucket_name,
                    e,
                )
                raise

    def enable_versioning(self):
        try:
            self.bucket.Versioning().enable()
            logger.info("Enabled versioning on bucket '%s'", self.bucket_name)
        except ClientError as e:
            logger.error(
                "Failed to enable versioning on bucket '%s': %s",
                self.bucket_name,
                e,
            )
            raise

    def upload_pdf(self, local_path: str, s3_key: str):
        logger.info(
            "Uploading '%s' to s3://%s/%s",
            local_path,
            self.bucket_name,
            s3_key,
        )
        self.bucket.upload_file(
            Filename=local_path,
            Key=s3_key,
            ExtraArgs={"ContentType": "application/pdf"},
        )
        logger.info("Upload completed for key '%s'", s3_key)

    def download_pdf(self, s3_key: str, local_path: str):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        logger.info(
            "Downloading s3://%s/%s to %s",
            self.bucket_name,
            s3_key,
            local_path,
        )
        self.bucket.download_file(s3_key, local_path)


