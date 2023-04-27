# @klotho::execution_unit {
#   id = "main"
# }

from fastapi import Body, FastAPI, Response, UploadFile, HTTPException
from app.persist import read_file, write_file, write_bytes, get_orm, get_redis, set_orm, set_redis
from app.persist_secret import get_secret
from app.crossexec.taskcombiner import combine_tasks
from starlette.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel

# @klotho::expose {
#   id = "py-gateway-primary"
#   target = "public"
# }
app = FastAPI()


@app.get("/test/exec/execute-cross-exec-tasks", response_class=JSONResponse)
async def get_cross_exec_tasks():
    return JSONResponse(content=await combine_tasks())


# TODO @app.get("/test/exec/execute-custom-dockerfile", ...)


@app.get("/test/persist-secret/read-binary-secret", response_class=PlainTextResponse)
async def get_secret_binary():
    return await get_secret(binary=True)


@app.get("/test/persist-secret/read-text-secret", response_class=PlainTextResponse)
async def get_secret_text():
    return await get_secret(binary=False)


@app.get("/test/persist-fs/read-text-file", response_class=PlainTextResponse)
async def read_text_file(path: str):
    return await read_file(path, binary=False)


@app.post("/test/persist-fs/write-text-file")
async def write_text_file(path: str, file: UploadFile):
    await write_file(path, file, binary=False)


@app.get("/test/persist-fs/read-binary-file")
async def read_binary_file(path: str):
    content = await read_file(path, binary=True)
    return Response(content=content, media_type="application/octet-stream")


@app.post("/test/persist-fs/write-binary-file-multipart")
async def write_binary_file(path: str, file: UploadFile):
    await write_file(path, file, binary=True)


@app.post("/test/persist-fs/write-binary-file-direct")
async def write_binary_file(path: str, file: bytes = Body()):
    await write_bytes(path, file)


class Item(BaseModel):
    key: str
    value: str


class CacheKey(BaseModel):
    key: str


@app.get("/test/persist-redis/redis-get-entry", response_class=JSONResponse)
async def get_redis_entry(key: CacheKey):
    v = await get_redis(key.key)
    if v is None:
        raise HTTPException(status_code=404, detail=f"{key.key} not found")
    return v


@app.post("/test/persist-redis/redis-set-entry")
async def set_redis_entry(item: Item):
    return await set_redis(item.key, item.value)


@app.get("/test/persist-orm/read-kv-entry")
async def get_orm_entry(key: str):
    v = await get_orm(key)
    if v is None:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    return v


@app.post("/test/persist-orm/write-kv-entry")
async def set_orm_entry(item: Item):
    return await set_orm(item.key, item.value)
