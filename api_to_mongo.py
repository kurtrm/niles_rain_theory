"""
Load data into mongo database.
"""
import requests

from pymongo import MongoClient
from typing import List, Dict


def load_mongo_db(db: str, collections: str, items: List[Dict]) -> None:
    """
    Load data into MongoDB.
    """
    mc = MongoClient()
    database = mc[db]
    collection = database[collections]
    collection.insert_many(items)
    mc.close()