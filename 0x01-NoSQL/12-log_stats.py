#!/usr/bin/env python3
"""Module for log status"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Display statistics about nginx logs stored in MongoDB.

    Args:
        mongo_collection: A pymongo collection object for 'nginx' logs.
    """
    # Total number of documents (logs)
    total_logs = mongo_collection.count_documents({})

    # Methods statistics
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_count = {}
    for method in methods:
        methods_count[method] =\
            mongo_collection.count_documents({"method": method})

    # Number of documents with specific method and path
    status_check_count =\
        mongo_collection.count_documents({"method": "GET", "path": "/status"})

    # Printing results
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    log_stats(nginx_collection)
