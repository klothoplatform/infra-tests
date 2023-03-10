# @klotho::execution_unit {
#   id = "main"
# }
from fastapi import FastAPI
from app.secret import get_secret
from app.crossexec.taskcombiner import combine_tasks

from starlette.responses import PlainTextResponse, JSONResponse

# @klotho::expose {
#   id = "py-gateway-primary"
#   target = "public"
# }
app = FastAPI()


@app.get("/test/exec/execute-cross-exec-tasks", response_class=JSONResponse)
async def get_cross_exec_tasks():
    return await combine_tasks()


# TODO @app.get("/test/exec/execute-custom-dockerfile", ...)


@app.get("/test/persist-secret/read-binary-secret", response_class=PlainTextResponse)
async def get_secret_binary():
    return await get_secret(binary=True)


@app.get("/test/persist-secret/read-text-secret", response_class=PlainTextResponse)
async def get_secret_text():
    return await get_secret(binary=False)
