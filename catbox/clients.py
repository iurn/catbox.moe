from io import BytesIO
from pathlib import Path

import httpx

from .constants import CATBOX_API, RequestTypes
from .exceptions import Failed, NoUserhash
from .albums import AlbumManager, AsyncAlbumManager


class Catbox:
    def __init__(self, userhash: str | None = None) -> None:
        """Initialize the Catbox client

        :param userhash: An optional userhash for requests to your account
        :type userhash: str or None
        """
        self.userhash = userhash
        self.album = AlbumManager(self.userhash)

    def upload(self, file_or_url: str | Path | BytesIO) -> str:
        """Upload a file or URL to Catbox

        :param file_or_url: The file path, file-like object, or URL to upload
        :type file_or_url: str or Path or BytesIO
        :return: The uploaded file URL
        :rtype: str
        """
        if isinstance(file_or_url, str) and file_or_url.startswith(
            ("http://", "https://")
        ):
            return self._upload_url(file_or_url)

        return self._upload_file(file_or_url)

    def _upload_url(self, url: str) -> str:
        """Upload a URL to Catbox

        :param url: The URL to upload
        :type url: str
        :return: The uploaded file URL
        :rtype: str
        """
        payload = {
            "reqtype": RequestTypes.urlupload,
            "url": url,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"URL upload failed: {response.status_code} {response.text}")

        return response.text.strip()

    def _upload_file(self, file: BytesIO | str | Path) -> str:
        """Upload a file to Catbox

        :param file: The file-like object or path to the file to upload
        :type file: BytesIO or str or Path
        :return: The uploaded file URL
        :rtype: str
        """
        payload = {
            "reqtype": RequestTypes.fileupload,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        if isinstance(file, (str, Path)):
            with open(file, "rb") as fp:
                response = httpx.post(
                    CATBOX_API,
                    data=payload,
                    files={"fileToUpload": fp},
                )
        else:
            response = httpx.post(
                CATBOX_API,
                data=payload,
                files={"fileToUpload": file},
            )

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"File upload failed: {response.status_code} {response.text}")

        return response.text.strip()

    def delete_files(self, files: str | list[str]) -> str:
        """Delete files from Catbox

        :param files: A file name or list of file names to delete
        :type files: str or list[str]
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to delete files")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": RequestTypes.deletefiles,
            "userhash": self.userhash,
            "files": files,
        }

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"File deletion failed: {response.status_code} {response.text}"
            )

        return response.text.strip()


class AsyncCatbox:
    def __init__(self, userhash: str | None = None) -> None:
        """Initialize the async Catbox client

        :param userhash: An optional userhash for requests to your account
        :type userhash: str or None
        """
        self.userhash = userhash
        self._client = httpx.AsyncClient()
        self.album = AsyncAlbumManager(self.userhash, client=self._client)

    async def upload(self, file_or_url: str | Path | BytesIO) -> str:
        """Upload a file or URL to Catbox

        :param file_or_url: The file path, file-like object, or URL to upload
        :type file_or_url: str or Path or BytesIO
        :return: The uploaded file URL
        :rtype: str
        """
        if isinstance(file_or_url, str) and file_or_url.startswith(
            ("http://", "https://")
        ):
            return await self._upload_url(file_or_url)

        return await self._upload_file(file_or_url)

    async def _upload_url(self, url: str) -> str:
        """Upload a URL to Catbox

        :param url: The URL to upload
        :type url: str
        :return: The uploaded file URL
        :rtype: str
        """
        payload = {
            "reqtype": RequestTypes.urlupload,
            "url": url,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        response = await self._client.post(
            CATBOX_API,
            data=payload,
        )

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"URL upload failed: {response.status_code} {response.text}")

        return response.text.strip()

    async def _upload_file(self, file: BytesIO | str | Path) -> str:
        """Upload a file to Catbox

        :param file: The file-like object or path to the file to upload
        :type file: BytesIO or str or Path
        :return: The uploaded file URL
        :rtype: str
        """
        payload = {
            "reqtype": RequestTypes.fileupload,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        if isinstance(file, (str, Path)):
            with open(file, "rb") as fp:
                response = await self._client.post(
                    CATBOX_API,
                    data=payload,
                    files={"fileToUpload": fp},
                )
        else:
            response = await self._client.post(
                CATBOX_API,
                data=payload,
                files={"fileToUpload": file},
            )

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"File upload failed: {response.status_code} {response.text}")

        return response.text.strip()

    async def delete_files(self, files: str | list[str]) -> str:
        """Delete files from Catbox

        :param files: A file name or list of file names to delete
        :type files: str or list[str]
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to delete files")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": RequestTypes.deletefiles,
            "userhash": self.userhash,
            "files": files,
        }

        response = await self._client.post(
            CATBOX_API,
            data=payload,
        )

        if response.status_code != 200:
            raise Failed(
                f"File deletion failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    async def close(self) -> None:
        """Close the async HTTP client"""
        await self._client.aclose()
