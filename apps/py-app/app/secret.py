# @klotho::persist {
#   id = "secrets"
#   secret = true
# }
import aiofiles as aio_secrets


async def get_secret(binary: bool = False):
    mode = 'r'
    if binary:
        mode += 'b'
    async with aio_secrets.open('secrets/secret.txt', mode=mode) as f:
        return await f.read()
