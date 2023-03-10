# @klotho::persist {
#   id = "files"
# }
import aiofiles as files
from fastapi import UploadFile
import redis.asyncio as redis
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import urllib.parse
from typing import Literal


# @klotho::persist {
#   id = "redis"
# }
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# @klotho::persist {
#   id = "sqlAlchemy"
# }
engine = create_engine("sqlite://")


async def read_file(path: str, binary: bool):
    path = _escape_path(path)
    async with files.open(path, mode=_mode('r', binary=binary)) as f:
        return await f.read()


async def write_file(path: str, contents: UploadFile, binary: bool):
    path = _escape_path(path)
    async with files.open(path, mode=_mode('w', binary=binary)) as f:
        file_data = await contents.read()
        if not binary:
            file_data = file_data.decode('utf8')
        await f.write(file_data)


async def write_bytes(path: str, contents: bytes):
    path = _escape_path(path)
    async with files.open(path, mode=_mode('w', binary=True)) as f:
        await f.write(contents)


async def delete_file(path: str):
    path = _escape_path(path)
    await files.os.remove(path)


def _mode(read_write: Literal['r', 'w'], binary: bool) -> Literal['r', 'rb', 'w', 'wb']:
    result = read_write
    if binary:
        result += 'b'
    print(f'mode: {result}')
    return result


async def get_redis(key: str):
    return {
        "key": key,
        "value": await redis_client.get(key),
    }


async def set_redis(key: str, value: str):
    return await redis_client.set(key, value)


class OrmBase(DeclarativeBase):
    pass


class OrmKV(OrmBase):
    __tablename__ = "kv"
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


OrmBase.metadata.create_all(engine)


async def get_orm(key: str):
    with Session(engine) as session:
        stmt = select(OrmKV).where(OrmKV.key == key)
        return session.scalars(stmt).one_or_none()


async def set_orm(key: str, value: str):
    with Session(engine) as session:
        kv = OrmKV(key=key, value=value)
        session.add(kv)
        session.commit()


def _escape_path(path: str) -> str:
    # see klothoplatform/klotho#360
    return urllib.parse.quote(path, safe='')
