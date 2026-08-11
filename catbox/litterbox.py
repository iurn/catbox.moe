from io import BytesIO
from pathlib import Path

import httpx

from .constants import LITTERBOX_API, VALID_LITTERBOX_HOURS, VALID_LITTERBOX_LENGTH, RequestTypes
from .exceptions import Failed, IncorrectTime


class Litterbox:
    def __init__(self) -> None:
        """Initialize the Litterbox client"""

    def upload(self, file: BytesIO | str | Path, hours: int = 1, namelength: int = 6) -> str:
        """Upload a file to Litterbox

        :param file: The file-like object or path to the file to upload
        :type file: BytesIO or str or Path
        :param hours: How long the file should be hosted
        :type hours: int
        :return: The uploaded file URL
        :rtype: str
        """
        if hours not in VALID_LITTERBOX_HOURS:
            raise IncorrectTime(
                f"Incorrect amount of hours. Must be one of {VALID_LITTERBOX_HOURS}"
            )

        if namelength not in VALID_LITTERBOX_LENGTH:
            raise IncorrectTime(
                f"Incorrect length. Must be one of {VALID_LITTERBOX_LENGTH}"
            )

        payload = {
            "reqtype": RequestTypes.fileupload,
            "time": f"{hours}h",
            "fileNameLength": namelength
        }

        if isinstance(file, (str, Path)):
            with open(file, "rb") as fp:
                response = httpx.post(
                    LITTERBOX_API,
                    data=payload,
                    files={"fileToUpload": fp},
                )
        else:
            response = httpx.post(
                LITTERBOX_API,
                data=payload,
                files={"fileToUpload": file},
            )

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"File upload failed: {response.status_code} {response.text}")

        return response.text.strip()


class AsyncLitterbox:
    def __init__(self) -> None:
        """Initialize the async Litterbox client"""
        self._client = httpx.AsyncClient()

    async def upload(self, file: BytesIO | str | Path, hours: int = 1, namelength: int = 6) -> str:
        """Upload a file to Litterbox

        :param file: The file-like object or path to the file to upload
        :type file: BytesIO or str or Path
        :param hours: How long the file should be hosted
        :type hours: int
        :return: The uploaded file URL
        :rtype: str
        """
        if hours not in VALID_LITTERBOX_HOURS:
            raise IncorrectTime(
                f"Incorrect amount of hours. Must be one of {VALID_LITTERBOX_HOURS}"
            )

        if namelength not in VALID_LITTERBOX_LENGTH:
            raise IncorrectTime(
                f"Incorrect length. Must be one of {VALID_LITTERBOX_LENGTH}"
            )

        payload = {
            "reqtype": RequestTypes.fileupload,
            "time": f"{hours}h",
            "fileNameLength": namelength
        }

        if isinstance(file, (str, Path)):
            with open(file, "rb") as fp:
                response = await self._client.post(
                    LITTERBOX_API,
                    data=payload,
                    files={"fileToUpload": fp},
                )
        else:
            response = await self._client.post(
                LITTERBOX_API,
                data=payload,
                files={"fileToUpload": file},
            )

        if response.status_code != 200 or not response.text.startswith("https://"):
            raise Failed(f"File upload failed: {response.status_code} {response.text}")

        return response.text.strip()

    async def close(self) -> None:
        """Close the async HTTP client"""
        await self._client.aclose()
