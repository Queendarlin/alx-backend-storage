#!/usr/bin/env python3
"""
Module for interacting with MongoDB to find top students by average score.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    Args:
        mongo_collection. The collection object from pymongo.

    Returns:
        list: A list of students with their average scores,
        sorted in descending order.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    return list(mongo_collection.aggregate(pipeline))
