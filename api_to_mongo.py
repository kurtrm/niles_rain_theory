"""
Load data into mongo database.
"""
import datetime
import requests
import yaml


from typing import List, Dict, Date

from pymongo import MongoClient


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

    start = datetime.date(2000, 1, 1)
    end = datetime.date(2018, 1, 1)
    dates = date_range(start, end)

    for date in dates:
        dated_url = url.format(date, date)
        response = requests.get(url=dated_url, headers=token)
        load_mongo_db('noaa', 'precipitation', response.json())


def load_mongo_db(db: str, collections: str, items: List[Dict]) -> None:
    """
    Load data into MongoDB.
    """
    mc = MongoClient()
    database = mc[db]
    collection = database[collections]
    collection.insert_many(items)
    mc.close()


def date_range(start: datetime.date, end: datetime.date) -> str:
    """
    Yield dates to pass to the url string.
    S/O for inspiration.
    """
    date_diff = int((end - start).days)
    for diff in range(date_diff):
        yield (start + datetime.timedelta(diff)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    main()
