from io import BytesIO
from uuid import uuid4
from functools import lru_cache

from minio import Minio

from app.core.config import settings


@lru_cache
def _get_client() -> Minio:
    client = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False,
    )
    bucket = settings.s3_bucket
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    return client


def upload_file(data: bytes, content_type: str, prefix: str = "") -> str:
    client = _get_client()
    bucket = settings.s3_bucket
    filename = f"{prefix}/{uuid4().hex}" if prefix else uuid4().hex
    client.put_object(bucket, filename, BytesIO(data), length=len(data), content_type=content_type)
    return f"{bucket}/{filename}"


def get_file_url(object_name: str) -> str:
    client = _get_client()
    return client.presigned_get_object(settings.s3_bucket, object_name)
