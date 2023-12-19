#!/usr/bin/env python3
"""
This module tests updating documents in mongodb
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})


if __name__ == "__main__":
    pass
