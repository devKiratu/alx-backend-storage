#!/usr/bin/env python3
"""
This module explores complex read queries with pymongo
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic
    """
    schools = []
    for school in mongo_collection.find({'topics': {'$in': [topic]}}):
        schools.append(school)

    return schools


if __name__ == "__main__":
    pass
