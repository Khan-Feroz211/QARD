"""Storage service: MinIO/S3 file upload and retrieval."""

import io
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.config import settings

_s3_client = None


def _get_client():
    """Return a lazily-initialised boto3 S3 client pointed at MinIO."""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
        )
    return _s3_client


def ensure_bucket() -> None:
    """Create the default bucket if it does not already exist."""
    client = _get_client()
    try:
        client.head_bucket(Bucket=settings.MINIO_BUCKET)
    except ClientError:
        client.create_bucket(Bucket=settings.MINIO_BUCKET)


async def upload_file(
    file_data: bytes,
    object_key: str,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload bytes to MinIO and return the public URL."""
    ensure_bucket()
    client = _get_client()
    client.put_object(
        Bucket=settings.MINIO_BUCKET,
        Key=object_key,
        Body=io.BytesIO(file_data),
        ContentType=content_type,
    )
    return f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_key}"


async def delete_file(object_key: str) -> None:
    """Delete an object from MinIO."""
    client = _get_client()
    try:
        client.delete_object(Bucket=settings.MINIO_BUCKET, Key=object_key)
    except ClientError:
        pass


async def generate_presigned_url(object_key: str, expires_in: int = 3600) -> str:
    """Return a pre-signed URL for temporary access to a private object."""
    client = _get_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.MINIO_BUCKET, "Key": object_key},
        ExpiresIn=expires_in,
    )
