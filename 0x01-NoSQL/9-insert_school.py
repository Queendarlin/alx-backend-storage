#!/usr/bin/env python3
"""
Module for Mongodb Insertion of document
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs.

        Args:
            mongo_collection: A pymongo collection object.
            **kwargs: Key-value pairs representing the document to be inserted

        Returns:
            The new _id of the inserted document.
    """
    docs = mongo_collection.insert_one(kwargs)
    return docs.inserted_id
