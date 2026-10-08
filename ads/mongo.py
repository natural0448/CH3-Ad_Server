"""Shared lazy MongoDB connection for the advertisement process."""
import atexit
from functools import lru_cache

from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_client():
    return MongoClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=3000,
        connectTimeoutMS=3000,
        appname="village-ads",
    )


def get_db():
    return get_client()[settings.MONGO_DB]


def close_client():
    if get_client.cache_info().currsize:
        get_client().close()
        get_client.cache_clear()


atexit.register(close_client)
