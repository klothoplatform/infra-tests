# @klotho::persist {
#   id = "pysecret"
#   secret = true
# }
import aiofiles as secrets
from app.persist import _mode


async def get_secret(binary: bool):
    async with secrets.open('secrets/secret.txt', mode=_mode('r', binary=binary)) as f:
        contents = await f.read()
        return contents
