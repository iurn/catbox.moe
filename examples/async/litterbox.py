import asyncio

from catbox import AsyncLitterbox


async def main() -> None:
    litterbox_client = AsyncLitterbox()

    await litterbox_client.upload("path/to/file.ext", hours=72)

    await litterbox_client.close()


asyncio.run(main())
