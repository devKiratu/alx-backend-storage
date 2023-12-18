#!/usr/bin/env python3
"""
This module contains a function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    Return a list of documents or an empty list if no document in the
    collection
    """
    result = []
    for doc in mongo_collection.find():
        result.append(doc)

    return result


if __name__ == '__main__':
    pass
