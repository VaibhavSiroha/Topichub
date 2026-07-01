"""Django file storage backend backed by Vercel Blob.

Vercel's serverless filesystem is read-only, so uploaded media (e.g. user
avatars) can't be written to disk. This backend uploads files to a Vercel Blob
store over its REST API and stores the returned public URL as the file name, so
templates can render it directly via ``{{ user.avatar.url }}``.

Requires the ``BLOB_READ_WRITE_TOKEN`` environment variable (added automatically
when you connect a Blob store to the Vercel project).
"""

from __future__ import annotations

import mimetypes
import os
from urllib.parse import quote

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

_API_BASE = "https://blob.vercel-storage.com"
_API_VERSION = "10"
_CACHE_MAX_AGE = "31536000"


@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self, token: str | None = None, prefix: str = "media") -> None:
        self._token = token
        self.prefix = prefix.strip("/")

    @property
    def token(self) -> str:
        token = self._token or os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not token:
            raise ValueError(
                "BLOB_READ_WRITE_TOKEN is not set; cannot upload to Vercel Blob."
            )
        return token

    def _pathname(self, name: str) -> str:
        name = name.lstrip("/")
        if self.prefix and not name.startswith(self.prefix + "/"):
            name = f"{self.prefix}/{name}"
        return name

    def _save(self, name: str, content) -> str:
        data = content.read()
        if isinstance(data, str):
            data = data.encode()

        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(name)[0]
            or "application/octet-stream"
        )

        pathname = self._pathname(name)
        resp = requests.put(
            f"{_API_BASE}/?pathname={quote(pathname)}",
            headers={
                "access": "public",
                "authorization": f"Bearer {self.token}",
                "x-api-version": _API_VERSION,
                "x-content-type": content_type,
                "x-cache-control-max-age": _CACHE_MAX_AGE,
                # Random suffix guarantees unique names (no cross-user overwrite).
                "x-add-random-suffix": "1",
            },
            data=data,
            timeout=30,
        )
        resp.raise_for_status()
        # Store the full public URL as the file "name" so url() is trivial.
        return resp.json()["url"]

    def url(self, name: str) -> str:
        if not name:
            return ""
        if name.startswith(("http://", "https://")):
            return name
        # Default avatar ("avatar.svg") and any legacy local names fall back to
        # the bundled static asset.
        return f"{settings.STATIC_URL}images/{name.lstrip('/')}"

    def exists(self, name: str) -> bool:
        # Random suffixes make names unique, so never treat as a collision.
        return False

    def get_available_name(self, name: str, max_length: int | None = None) -> str:
        return name

    def size(self, name: str) -> int:
        return 0

    def _open(self, name: str, mode: str = "rb"):
        resp = requests.get(self.url(name), timeout=30)
        resp.raise_for_status()
        return ContentFile(resp.content, name=name)

    def delete(self, name: str) -> None:
        if name and name.startswith("http"):
            try:
                requests.post(
                    f"{_API_BASE}/delete",
                    headers={
                        "authorization": f"Bearer {self.token}",
                        "x-api-version": _API_VERSION,
                    },
                    json={"urls": [name]},
                    timeout=10,
                )
            except requests.RequestException:
                pass
