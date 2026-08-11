import asyncio

from catbox import AsyncAlbumManager


async def main() -> None:
    album_manager = AsyncAlbumManager(userhash="your_userhash")

    album_short = await album_manager.create(
        "My Album", "A description", files=["file1.ext"]
    )
    await album_manager.add(album_short, ["file2.ext"])
    await album_manager.remove(album_short, ["file1.ext"])
    await album_manager.delete(album_short)

    await album_manager.close()


asyncio.run(main())
