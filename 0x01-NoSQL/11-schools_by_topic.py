#!/usr/bin/env python3
"""
Module for finding documents in Mongodb
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: A pymongo collection object.
        topic (string): The topic to search for.

    Returns:
        list: List of documents (dictionaries)
        from the collection that match the topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
