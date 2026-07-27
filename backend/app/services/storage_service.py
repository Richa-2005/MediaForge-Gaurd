from pathlib import Path
from urllib.parse import quote

import httpx
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


def supabase_storage_enabled() -> bool:
    return bool(
        settings.SUPABASE_URL
        and settings.SUPABASE_STORAGE_BUCKET
        and settings.SUPABASE_SERVICE_ROLE_KEY.get_secret_value()
    )


def build_storage_key(media_id: str, filename: str) -> str:
    extension = Path(filename).suffix.lower()
    return f"uploads/{media_id}/{media_id}{extension}"


def _object_url(object_key: str) -> str:
    bucket = quote(settings.SUPABASE_STORAGE_BUCKET, safe="")
    key = quote(object_key, safe="/")
    return (
        f"{settings.SUPABASE_URL.rstrip('/')}"
        f"/storage/v1/object/{bucket}/{key}"
    )


def _headers(content_type: str | None = None) -> dict[str, str]:
    service_key = settings.SUPABASE_SERVICE_ROLE_KEY.get_secret_value()
    headers = {
        "Authorization": f"Bearer {service_key}",
        "apikey": service_key,
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


async def upload_to_supabase_storage(
    uploaded_file: UploadFile,
    object_key: str,
    content_type: str,
) -> None:
    if not supabase_storage_enabled():
        return

    await uploaded_file.seek(0)
    data = await uploaded_file.read()
    await uploaded_file.seek(0)

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            _object_url(object_key),
            headers={
                **_headers(content_type),
                "x-upsert": "true",
            },
            content=data,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "The media could not be stored in Supabase Storage. "
                f"Supabase returned {response.status_code}."
            ),
        )


def download_from_supabase_storage(object_key: str) -> tuple[bytes, str | None]:
    if not supabase_storage_enabled():
        raise FileNotFoundError("Supabase Storage is not configured.")

    with httpx.Client(timeout=60.0) as client:
        response = client.get(
            _object_url(object_key),
            headers=_headers(),
        )

    if response.status_code == 404:
        raise FileNotFoundError(object_key)
    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The media could not be loaded from Supabase Storage.",
        )

    return response.content, response.headers.get("content-type")
