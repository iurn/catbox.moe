import httpx

from .constants import CATBOX_API, AlbumRequestTypes
from .exceptions import Failed, NoUserhash


class AlbumManager:
    def __init__(self, userhash: str | None = None) -> None:
        """Initialize the album manager

        :param userhash: An optional userhash for requests to your account
        :type userhash: str or None
        """
        self.userhash = userhash

    def create(self, title: str, desc: str, files: str | list | None = None) -> str:
        """Create an album on Catbox

        :param title: The title of the album
        :type title: str
        :param desc: The description of the album
        :type desc: str
        :param files: A file name or list of file names to add
        :type files: str or list or None
        :return: The album's short identifier
        :rtype: str
        """
        payload = {
            "reqtype": AlbumRequestTypes.create,
            "title": title,
            "desc": desc,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        if isinstance(files, list):
            files = " ".join(files)

        payload["files"] = files

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album creation failed: {response.status_code} {response.text}"
            )

        return response.text.strip().rsplit("/", 1)[-1]

    def edit(self, short: str, title: str, desc: str, files: str | list) -> str:
        """Edit an album on Catbox

        :param short: The short identifier of the album
        :type short: str
        :param title: The new title of the album
        :type title: str
        :param desc: The new description of the album
        :type desc: str
        :param files: A file name or list of file names for the album
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to edit albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.edit,
            "userhash": self.userhash,
            "short": short,
            "title": title,
            "desc": desc,
            "files": files,
        }

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album editing failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    def add(self, short: str, files: str | list) -> str:
        """Add files to an album

        :param short: The short identifier of the album
        :type short: str
        :param files: A file name or list of file names to add
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to add files to albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.add,
            "userhash": self.userhash,
            "short": short,
            "files": files,
        }

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(f"Album adding failed: {response.status_code} {response.text}")

        return response.text.strip()

    def remove(self, short: str, files: str | list) -> str:
        """Remove files from an album

        :param short: The short identifier of the album
        :type short: str
        :param files: A file name or list of file names to remove
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to remove files from albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.remove,
            "userhash": self.userhash,
            "short": short,
            "files": files,
        }

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album removing failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    def delete(self, short: str) -> str:
        """Delete an album from Catbox

        :param short: The short identifier of the album
        :type short: str
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to delete albums")

        payload = {
            "reqtype": AlbumRequestTypes.delete,
            "userhash": self.userhash,
            "short": short,
        }

        response = httpx.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album deleting failed: {response.status_code} {response.text}"
            )

        return response.text.strip()


class AsyncAlbumManager:
    def __init__(
        self,
        userhash: str | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize the async album manager

        :param userhash: An optional userhash for requests to your account
        :type userhash: str or None
        :param client: An optional shared async HTTP client
        :type client: httpx.AsyncClient or None
        """
        self.userhash = userhash
        self._client = client or httpx.AsyncClient()

    async def create(
        self, title: str, desc: str, files: str | list | None = None
    ) -> str:
        """Create an album on Catbox

        :param title: The title of the album
        :type title: str
        :param desc: The description of the album
        :type desc: str
        :param files: A file name or list of file names to add
        :type files: str or list or None
        :return: The album's short identifier
        :rtype: str
        """
        payload = {
            "reqtype": AlbumRequestTypes.create,
            "title": title,
            "desc": desc,
        }

        if self.userhash:
            payload["userhash"] = self.userhash

        if isinstance(files, list):
            files = " ".join(files)

        payload["files"] = files

        response = await self._client.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album creation failed: {response.status_code} {response.text}"
            )

        return response.text.strip().rsplit("/", 1)[-1]

    async def edit(self, short: str, title: str, desc: str, files: str | list) -> str:
        """Edit an album on Catbox

        :param short: The short identifier of the album
        :type short: str
        :param title: The new title of the album
        :type title: str
        :param desc: The new description of the album
        :type desc: str
        :param files: A file name or list of file names for the album
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to edit albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.edit,
            "userhash": self.userhash,
            "short": short,
            "title": title,
            "desc": desc,
            "files": files,
        }

        response = await self._client.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album editing failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    async def add(self, short: str, files: str | list) -> str:
        """Add files to an album

        :param short: The short identifier of the album
        :type short: str
        :param files: A file name or list of file names to add
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to add files to albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.add,
            "userhash": self.userhash,
            "short": short,
            "files": files,
        }

        response = await self._client.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(f"Album adding failed: {response.status_code} {response.text}")

        return response.text.strip()

    async def remove(self, short: str, files: str | list) -> str:
        """Remove files from an album

        :param short: The short identifier of the album
        :type short: str
        :param files: A file name or list of file names to remove
        :type files: str or list
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to remove files from albums")

        if isinstance(files, list):
            files = " ".join(files)

        payload = {
            "reqtype": AlbumRequestTypes.remove,
            "userhash": self.userhash,
            "short": short,
            "files": files,
        }

        response = await self._client.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album removing failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    async def delete(self, short: str) -> str:
        """Delete an album from Catbox

        :param short: The short identifier of the album
        :type short: str
        :return: The response from Catbox
        :rtype: str
        :raises NoUserhash: If no userhash is provided
        """
        if not self.userhash:
            raise NoUserhash("A userhash is required to delete albums")

        payload = {
            "reqtype": AlbumRequestTypes.delete,
            "userhash": self.userhash,
            "short": short,
        }

        response = await self._client.post(CATBOX_API, data=payload)

        if response.status_code != 200:
            raise Failed(
                f"Album deleting failed: {response.status_code} {response.text}"
            )

        return response.text.strip()

    async def close(self) -> None:
        """Close the async HTTP client"""
        await self._client.aclose()
