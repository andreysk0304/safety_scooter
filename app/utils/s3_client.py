import asyncio
import logging
import os
from uuid import uuid4

import boto3

from botocore.exceptions import ClientError

from botocore.client import Config
from fastapi import UploadFile

from app.utils.config import S3_BUCKET, S3_ENDPOINT_URL, S3_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# ИСПРАВЛЕНО: создание клиента вынесено в функцию для ленивой инициализации
def get_s3_client():
    """Получение S3 клиента (создается при первом использовании)"""
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION_NAME,
        config=Config(signature_version="s3v4")
    )


class S3Client:

    @staticmethod
    async def upload_video(file: UploadFile) -> str:
        """
        Асинхронная загрузка видео в S3
        Использует asyncio.to_thread для выполнения синхронной операции boto3 в отдельном потоке
        """
        try:
            if not file.filename:
                logging.error('S3_upload_video: filename is None')
                return "null"
                
            clean_filename = os.path.basename(file.filename)
            clean_filename = clean_filename.replace(" ", "_")

            key = f"safetyscooter_videos/{uuid4()}_{clean_filename}"

            file.file.seek(0)

            # ИСПРАВЛЕНО: выполнение синхронной операции в отдельном потоке
            s3 = get_s3_client()
            await asyncio.to_thread(
                s3.upload_fileobj,
                file.file,
                S3_BUCKET,
                key,
                ExtraArgs={"ContentType": "video/mp4"}
            )

            logging.info(f'S3_upload_video: успешно загружено {key}')
            return key

        except Exception as error:
            logging.error(f'S3_upload_video: {error}', exc_info=True)
            return "null"


    @staticmethod
    async def generate_presigned_url(key: str, expires_in: int = 600) -> str:
        """
        Генерация presigned URL для скачивания файла
        """
        try:
            if not key or key == "null":
                logging.error('S3_generate_presigned_url: invalid key')
                return 'null'
                
            s3 = get_s3_client()
            # ИСПРАВЛЕНО: выполнение синхронной операции в отдельном потоке
            url = await asyncio.to_thread(
                s3.generate_presigned_url,
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logging.error(f'S3_generate_presigned_url: {e}', exc_info=True)
            return 'null'
        except Exception as e:
            logging.error(f'S3_generate_presigned_url: unexpected error {e}', exc_info=True)
            return 'null'