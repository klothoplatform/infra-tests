# @klotho::persist {
#   id = "pysecret"
#   secret = true
# }
import aiofiles as secrets
# @klotho::persist {
#   id = "files"
# }
import aiofiles as files
from asyncio import StreamReader
from fastapi import UploadFile
from typing import Literal, Union


async def get_secret(binary: bool):
    async with secrets.open('secrets/secret.txt', mode=_mode('r', binary=binary)) as f:
        contents = await f.read()
        return contents


async def read_file(path: str, binary: bool):
    async with files.open(path, mode=_mode('r', binary=binary)) as f:
        return await f.read()


async def write_file(path: str, contents: UploadFile, binary: bool):
    async with files.open(path, mode=_mode('w', binary=binary)) as f:
        file_data = await contents.read()
        if not binary:
            file_data = file_data.decode('utf8')
        await f.write(file_data)


async def write_bytes(path: str, contents: bytes):
    async with files.open(path, mode=_mode('w', binary=True)) as f:
        await f.write(contents)


async def delete_file(path: str):
    await files.os.remove(path)


def _mode(read_write: Literal['r', 'w'], binary: bool) -> Literal['r', 'rb', 'w', 'wb']:
    result = read_write
    if binary:
        result += 'b'
    return result
