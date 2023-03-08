from fastapi import FastAPI
from app.secret import get_secret

from starlette.responses import PlainTextResponse

# @klotho::expose {
#   id = "redis-gw"
#   target = "public"
# }
app = FastAPI()


@app.get("/test/persist-secret/read-binary-secret")
async def get_secret_binary():
    return await get_secret(binary=True)


@app.get("/test/persist-secret/read-text-secret", response_class=PlainTextResponse)
async def get_secret_text():
    return await get_secret()
