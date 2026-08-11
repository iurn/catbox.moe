import asyncio

from catbox import AsyncCatbox


async def main() -> None:
    catbox_client = AsyncCatbox(userhash="your_userhash")

    await catbox_client.upload("path/to/file.ext")
    await catbox_client.upload("https://example.com/image.png")
    await catbox_client.delete_files(["file1.ext", "file2.ext"])

    await catbox_client.close()


asyncio.run(main())
