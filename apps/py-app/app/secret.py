# @klotho::persist {
#   id = "pysecret"
#   secret = true
# }
import aiofiles as secrets


async def get_binary_secret():
    async with secrets.open('secrets/secret.txt', mode='rb') as f:
        contents = await f.read()
        return contents


async def get_text_secret():
    async with secrets.open('secrets/secret.txt', mode='r') as f:
        contents = await f.read()
        return contents
