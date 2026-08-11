from catbox import Catbox

catbox_client = Catbox(userhash="your_userhash")

catbox_client.upload("path/to/file.ext")
catbox_client.upload("https://example.com/image.png")
catbox_client.delete_files(["file1.ext", "file2.ext"])
