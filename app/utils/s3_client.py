import logging
from uuid import uuid4

import boto3

from botocore.exceptions import ClientError

from botocore.client import Config
from fastapi import UploadFile

from app.utils.config import S3_BUCKET, S3_ENDPOINT_URL, S3_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=S3_ENDPOINT_URL,
    region_name=S3_REGION_NAME,
    config=Config(signature_version="s3v4")
)


class S3Client:

    @staticmethod
    def upload_video(file: UploadFile) -> str:
        try:
            key = f"safetyscooter_videos/{uuid4()}_{file.filename}"

            s3.upload_fileobj(
                file.file,
                S3_BUCKET,
                key,
                ExtraArgs={"ContentType": "video/mp4"}
            )

            return key

        except Exception as error:
            logging.error(f'S3_upload_video: {error}')

            return "null"

    @staticmethod
    def generate_presigned_url(key: str, expires_in: int = 600) -> str:
        try:
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError:
            return 'null'