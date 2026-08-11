<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://catbox.moe/pictures/logo_white.png">
    <source media="(prefers-color-scheme: light)" srcset="https://catbox.moe/pictures/logo.png">
    <img alt="catbox" src="https://catbox.moe/pictures/logo.png">
  </picture>
</div>

<h1 align="center">catbox.moe</h1>

<p align="center">
  A simple, async &amp; sync Python wrapper for the <a href="https://catbox.moe">Catbox</a> and <a href="https://litterbox.catbox.moe">Litterbox</a> APIs.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dependencies-httpx-blueviolet" alt="httpx">
</p>

---

## Features

- Sync and async clients for [Catbox](https://catbox.moe)
- Temporary uploads via [Litterbox](https://litterbox.catbox.moe)
- Full album management (create, edit, add, remove, delete)
- Upload from file paths, URLs, or file-like objects
- Type hints and clean exception types

## Installation

```bash
pip install catbox.moe
```

Or install from source:

```bash
git clone https://github.com/iurn/catbox.moe
cd catbox.moe
pip install .
```

## Quick Start

### Synchronous

```python
from catbox import Catbox

catbox_client = Catbox(userhash="your_userhash")

catbox_client.upload("path/to/file.ext")
catbox_client.upload("https://example.com/image.png")
catbox_client.delete_files(["file1.ext", "file2.ext"])
```

### Asynchronous

```python
import asyncio

from catbox import AsyncCatbox


async def main() -> None:
    catbox_client = AsyncCatbox(userhash="your_userhash")

    await catbox_client.upload("path/to/file.ext")
    await catbox_client.upload("https://example.com/image.png")
    await catbox_client.delete_files(["file1.ext", "file2.ext"])

    await catbox_client.close()


asyncio.run(main())
```

The `userhash` is optional and only needed for account-scoped actions such as deleting files.

## Litterbox

[Litterbox](https://litterbox.catbox.moe) is Catbox's service for temporary files. Files can be hosted for `1`, `12`, `24`, or `72` hours.

```python
from catbox import Litterbox

litterbox_client = Litterbox()

litterbox_client.upload("path/to/file.ext", hours=24)
```

## Album Management

`create` returns the album's short identifier, which is used by the other album methods.

```python
from catbox import AlbumManager

album_manager = AlbumManager(userhash="your_userhash")

album_short = album_manager.create("My Album", "A description", files=["file1.ext"])
album_manager.add(album_short, ["file2.ext"])
album_manager.remove(album_short, ["file1.ext"])
album_manager.delete(album_short)
```

## API Reference

### `catbox.Catbox` / `catbox.AsyncCatbox`

| Method | Description |
| --- | --- |
| `upload(file_or_url)` | Upload a file path, URL, or file-like object. Returns the uploaded file URL. |
| `delete_files(files)` | Delete one or more files. Requires a `userhash`. |

### `catbox.Litterbox` / `catbox.AsyncLitterbox`

| Method | Description |
| --- | --- |
| `upload(file, hours=1)` | Upload a temporary file. `hours` must be one of `1`, `12`, `24`, `72`. |

### `catbox.AlbumManager` / `catbox.AsyncAlbumManager`

| Method | Description |
| --- | --- |
| `create(title, desc, files=None)` | Create an album. Returns the album's short identifier. |
| `edit(short, title, desc, files)` | Update an album's details. |
| `add(short, files)` | Add files to an album. |
| `remove(short, files)` | Remove files from an album. |
| `delete(short)` | Delete an album. |

All async clients expose a `close()` method to shut down their internal HTTP client.

## Exceptions

| Exception | Raised when |
| --- | --- |
| `catbox.exceptions.Failed` | The API request failed (non-200 response). |
| `catbox.exceptions.NoUserhash` | An account-scoped action was attempted without a `userhash`. |
| `catbox.exceptions.IncorrectTime` | An invalid Litterbox expiration time was provided. |

## Examples

More runnable examples are available in the [examples](examples) folder, split by sync and async.

## License

Distributed under the [MIT License](LICENSE).
