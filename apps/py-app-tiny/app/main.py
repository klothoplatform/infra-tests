# @klotho::execution_unit {
#   id = "main"
# }

from fastapi import Body, FastAPI, Response, UploadFile, HTTPException
from starlette.responses import PlainTextResponse, JSONResponse

# @klotho::expose {
#   id = "py-gateway-primary"
#   target = "public"
# }
app = FastAPI()


@app.get("/test/persist-fs/read-text-file", response_class=PlainTextResponse)
async def get_secret_text():
    return "hello"


@app.post("/test/persist-fs/write-text-file")
async def write_text_file(path: str, file: UploadFile):
    pass
