from enum import StrEnum

CATBOX_API = "https://catbox.moe/user/api.php"
LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"
VALID_LITTERBOX_HOURS = [1, 12, 24, 72]
VALID_LITTERBOX_LENGTH = [6, 16]


class RequestTypes(StrEnum):
    urlupload = "urlupload"
    fileupload = "fileupload"
    deletefiles = "deletefiles"


class AlbumRequestTypes(StrEnum):
    create = "createalbum"
    edit = "editalbum"
    add = "addtoalbum"
    remove = "removefromalbum"
    delete = "deletealbum"
