"""
Load data into mongo database.
"""
import requests
import yaml

from typing import List, Dict

from pymongo import MongoClient


def load_mongo_db(db: str, collections: str, items: List[Dict]) -> None:
    """
    Load data into MongoDB.
    """
    mc = MongoClient()
    database = mc[db]
    collection = database[collections]
    collection.insert_many(items)
    mc.close()


def main():
    """
    Load stuff from api.
    """
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
    '?datasetid=GHCND'
    '&locationid=CITY:US530018'
    '&startdate={}'
    '&enddate={}'

    with open('.secrets/noaa_api_key.yaml') as f:
        token = yaml.load(f)

    response = requests.get(url=url, params=None, headers=token)
