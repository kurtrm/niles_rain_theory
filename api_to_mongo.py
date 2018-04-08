"""
Load data into mongo database.
"""
import datetime
import requests
import time
import yaml


from typing import List, Dict

from pymongo import MongoClient


def main():
    """
    Load stuff from api.
    """
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data' \
          '?datasetid=GHCND' \
          '&locationid=CITY:US530018' \
          '&units=STANDARD' \
          '&startdate=2000-01-01' \
          '&enddate=2018-01-01' \
          '&limit=1000' \
          '&offset={}'

    with open('/home/kurtrm/.secrets/noaa_api_key.yaml') as f:
        token = yaml.load(f)

    offset = 1

    status = 200

    while status == 200:
        offset_url = url.format(offset)
        response = requests.get(url=offset_url, headers=token)
        status = response.status_code
        # import pdb; pdb.set_trace()
        if status == 200 and response.content:
            print(f"Loading {offset}")
            load_mongo_db('noaa', 'precipitation', response.json()['results'])
            offset += 1000


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
    date_diff = int((end - start).months)
    for diff in range(date_diff):
        yield (start + datetime.timedelta(diff)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    main()
