import pydantic
import datetime

from api.database.db import DB

from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import UJSONResponse

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from bson import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


router = APIRouter(prefix="/api")


# @router.post("/leading")
# def get_leading_offerts(
#         offset: int = 0,
#         limit: int = 20,
#         sorting: Sorting | None = None,
#         filters: Filtering | None = None):
#     return DB.get_leading_offerts(offset, limit, sorting)


# @ router.get("/detailed/{offert_id}")
# def get_detailed_offert(offert_id: str):
#     return DB.get_detailed_offert(offert_id)


# @ router.get("/count")
# def get_offerts_count():
#     return {"count": DB.get_offerts_count()}


@cache()
async def get_cache():
    return 1


@router.get("/raw/last")
@cache(expire=60)
async def get_last_grades():
    """
    Returns the last grades from the database

    Should be used for debugging purposes only!    
    """

    return UJSONResponse(content=jsonable_encoder(DB.get_last_grades_from_db()))


@router.get("/difference/today")
@cache(expire=60)
async def get_difference_today():
    """
    Returns the difference between yesterday's grades and today's grades
    """

    r = DB.get_difference_from_today()

    if r == None or len(r) == 0:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/difference/day/{date}")
@cache(expire=60)
async def get_difference_date(date: str):
    """
    Returns the difference between yesterday's grades and today's grades

    Date format: YYYY-MM-DD

    For example: 2021-10-02 compares grades from 2021-10-01 with grades from 2021-10-02
    """

    r = DB.get_difference_from_date(date)

    if r == None or len(r) == 0:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/difference/week/{date}")
@cache(expire=60)
async def get_difference_week(date: str):
    """
    Returns the difference between today-7 days grades

    Date format: YYYY-MM-DD

    For example: 2021-10-02 compares grades from 2021-09-25 with grades from 2021-10-02
    """

    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = date - datetime.timedelta(days=7)

    r = []

    for i in range(7):
        date = date + datetime.timedelta(days=1)

        x = DB.get_difference_from_date(date.strftime("%Y-%m-%d"))

        if x != None:
            r.append({"date": date.strftime("%Y-%m-%d"), "nd": i, "grades": x})
        else:
            continue

    if r == None or len(r) == 0:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/difference/month/{date}")
@cache(expire=300)
async def get_difference_month(date: str):
    """
    Returns the difference between today-30 days grades

    Date format: YYYY-MM-DD

    (long execution time xdxdxd)
    """

    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = date - datetime.timedelta(days=30)

    r = []

    for i in range(30):
        date = date + datetime.timedelta(days=1)

        x = DB.get_difference_from_date(date.strftime("%Y-%m-%d"))

        if x != None:
            r.append({"date": date.strftime("%Y-%m-%d"), "nd": i, "grades": x})
        else:
            continue

    if r == None or len(r) == 0:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
