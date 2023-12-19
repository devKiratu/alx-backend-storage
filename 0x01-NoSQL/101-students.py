#!/usr/bin/env python3
"""
Querying and data aggregation in mongodb using pymongo
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    results = []
    students = mongo_collection.aggregate([
        {
            '$project': {
                'name': '$name',
                'totalScore': {
                    '$map': {
                        'input': '$topics',
                        'as': 'topic',
                        'in': {'$sum': '$$topic.score'}
                        }
                    },
                },
        },
        {
            '$project': {
                'name': '$name',
                'averageScore': {
                    '$avg': '$totalScore'
                }
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ])

    for student in students:
        results.append(student)
    return results
