from io import BytesIO
from uuid import uuid4

from minio import Minio

from app.core.config import settings

_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False,
)

_bucket = settings.s3_bucket

if not _client.bucket_exists(_bucket):
    _client.make_bucket(_bucket)


def upload_file(data: bytes, content_type: str, prefix: str = "") -> str:
    filename = f"{prefix}/{uuid4().hex}" if prefix else uuid4().hex
    _client.put_object(_bucket, filename, BytesIO(data), length=len(data), content_type=content_type)
    return f"{_bucket}/{filename}"


def get_file_url(object_name: str) -> str:
    return _client.presigned_get_object(_bucket, object_name)
