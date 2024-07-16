#!/usr/bin/env python3
"""
Module to print stats from a MongoDB collection named
'nginx' in the 'logs' database.
"""

from pymongo import MongoClient


def log_stats():
    """
    Prints log statistics from the MongoDB collection.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of logs with status check
    status_check_count = collection.count_documents({"method": "GET",
                                                     "path": "/status"})
    print(f"{status_check_count} status check")

    # Top 10 most present IPs
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 10
        }
    ]
    top_ips = collection.aggregate(pipeline)
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
