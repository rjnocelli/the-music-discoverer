import httpx
from enum import auto
from fastapi_utils.enums import StrEnum

class HttpVerbs(StrEnum):
    get = auto()
    post = auto()
    put = auto()
    delete = auto()

class BaseHttpClient:
    async def _make_request(verb: HttpVerbs, url: str):
        resp = await getattr(httpx, verb.value)(url)
        return resp.json()