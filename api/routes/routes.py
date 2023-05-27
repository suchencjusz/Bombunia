import pydantic
import datetime

from api.database.db import DB
from utils import datetime_input_checker_n_parser
from bombunia import bombunia_manager as bmb

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


@cache()
async def get_cache():
    return 1


@router.get("/difference/today")
async def get_difference_today():
    """
    Returns the difference between yesterday's grades and today's grades
    """

    r = DB.get_difference_from_today()

    if r == None or len(r) == 0:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/difference/day/{date}")
@cache(expire=300)
async def get_difference_date(date: str):
    """
    Returns the difference between yesterday's grades and today's grades

    Date format: YYYY-MM-DD

    For example: 2021-10-02 compares grades from 2021-10-01 with grades from 2021-10-02
    """

    date = datetime_input_checker_n_parser(date)

    if date["failed"]:
        return UJSONResponse(status_code=400, content=jsonable_encoder(date))

    date = date["status"]

    r = DB.get_difference_from_date(date)

    if r == None:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/difference/week/{date}")
@cache(expire=300)
async def get_difference_week(date: str):
    """
    Returns the difference between today-7 days grades

    Date format: YYYY-MM-DD

    For example: 2021-10-02 compares grades from 2021-09-25 with grades from 2021-10-02
    """
    date = datetime_input_checker_n_parser(date)

    if date["failed"]:
        return UJSONResponse(status_code=400, content=jsonable_encoder(date))

    date = date["status"]

    r = bmb.Bombunia.get_difference_in_days(date, 7, _db=DB.db)

    if r == None or r == []:
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

    date = datetime_input_checker_n_parser(date)

    if date["failed"]:
        return UJSONResponse(status_code=400, content=jsonable_encoder(date))

    date = date["status"]

    r = bmb.Bombunia.get_difference_in_days(date, 30, _db=DB.db)

    if r == None or r == []:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.get("/raw/heatmap/week/{date}")
# @cache(expire=300)
async def get_raw_heatmap_week(date: str):
    """
    Returns the difference between today-7 days grades

    Date format: YYYY-MM-DD

    For example: 2021-10-02 compares grades from 2021-09-25 with grades from 2021-10-02
    """

    date = datetime_input_checker_n_parser(date)

    if date["failed"]:
        return UJSONResponse(status_code=400, content=jsonable_encoder(date))

    date = date["status"]
   
    r = bmb.Bombunia.get_difference_in_days(date, 7, _db=DB.db)

    if r == None or r == []:
        return Response(status_code=204)

    bmb.Bombunia.generate_heatmap(r)

    return UJSONResponse(content=jsonable_encoder(r))

# @router.get("/difference_a/from/{date_from}/{date_to}")
# @cache(expire=300)
# async def get_difference_a(date_from: str, date_to: str):
#     """
#     Returns the difference between two dates

#     Date format: YYYY-MM-DD

#     For example: 2021-10-02 compares grades from 2021-10-01 with grades from 2021-10-02
#     """

#     date_from = datetime_input_checker_n_parser(date_from)
#     date_to = datetime_input_checker_n_parser(date_to)

#     if date_from["failed"] or date_to["failed"]:
#         return UJSONResponse(status_code=400, content=jsonable_encoder(date_from)) # !!!

#     r = DB.get_difference_from_month_aggregation(date_from, date_to)

#     if r == None or len(r) == 0:
#         return Response(status_code=204)

#     return UJSONResponse(content=jsonable_encoder(r))


@router.get("/average/all")
@cache(expire=300)
async def get_average_all():
    """
    Returns the average grade for each day of the month

    c - is count of grades
    """

    r = DB.get_average_all()

    if r == None or r == []:
        return Response(status_code=204)

    return UJSONResponse(content=jsonable_encoder(r))


@router.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
