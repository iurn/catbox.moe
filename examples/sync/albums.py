from catbox import AlbumManager

album_manager = AlbumManager(userhash="your_userhash")

album_short = album_manager.create("My Album", "A description", files=["file1.ext"])
album_manager.add(album_short, ["file2.ext"])
album_manager.remove(album_short, ["file1.ext"])
album_manager.delete(album_short)
