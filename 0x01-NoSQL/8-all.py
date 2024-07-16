#!/usr/bin/env python3
"""
 Module for a Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """Lists all documents in a collection.

       Args:
           mongo_collection: A pymongo collection object.

       Returns:
           A list of all documents in the collection.
           Returns an empty list if no documents are found.
    """
    if mongo_collection is not None:
        return list(mongo_collection.find())
    else:
        return []
