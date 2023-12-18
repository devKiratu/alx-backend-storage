#!/usr/bin/env python3
"""
This module contains a function for inserting a new document in mongodb
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection based on kwargs and returns
    the id of inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id


if __name__ == "__main__":
    pass
