import mimetypes
from pathlib import Path

import aiofiles
import werkzeug

from userdata_api import config


async def save_photo(user_id: int, photo: werkzeug.datastructures.FileStorage) -> Path:
    photos_dir = config.PHOTOS_PATH_BASE
    if photos_dir.exists() is False:
        photos_dir.mkdir()
    mimetype = photo.stream.type
    mimetype = mimetype
    if mimetype.startswith("image") is False:
        mimetype_guessed = mimetypes.guess_type(photo.stream.name)[0]
        if mimetype_guessed is not None and mimetype_guessed.startswith("image") is True:
            mimetype = mimetype_guessed
    ext = mimetypes.guess_extension(mimetype)
    path = photos_dir / f"{user_id}{ext}"
    async with aiofiles.open(path, "wb") as f:
        await f.write(photo.stream.body)
    return path


def get_photo_url(relative_path: str):
    return f"{config.PHOTOS_PUBLIC_URL_BASE}/{relative_path}"


def delete_photo(relative_path: str):
    path = Path.cwd() / relative_path
    if path.exists() is True:
        path.unlink()
