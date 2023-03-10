# @klotho::persist {
#   id = "pysecret"
#   secret = true
# }
import aiofiles as secrets
from typing import Literal


async def get_secret(binary: bool):
    mode: Literal['r', 'rb'] = 'r'
    if binary:
        mode = 'rb'
    async with secrets.open('secrets/secret.txt', mode=mode) as f:
        contents = await f.read()
        return contents
