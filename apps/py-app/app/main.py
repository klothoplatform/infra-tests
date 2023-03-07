from fastapi import FastAPI
from app import secret

from starlette.responses import PlainTextResponse

# @klotho::expose {
#   id = "redis-gw"
#   target = "public"
# }
app = FastAPI()


@app.get("/test/persist-secret/read-binary-secret")
async def get_secret_binary():
    return await secret.get_secret(binary=True)


@app.get("/test/persist-secret/read-text-secret", response_class=PlainTextResponse)
async def get_secret_text():
    return await secret.get_secret()
