#!/usr/bin/env python3
"""
Analyze nginx logs stored in mongodb
Database: logs
Collection: nginx
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """
    Query, organize and print formatted results
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # get total logs
    total_logs = nginx_collection.count_documents({})

    # get logs by method
    get_results = nginx_collection.count_documents({'method': 'GET'})
    post_results = nginx_collection.count_documents({'method': 'POST'})
    put_results = nginx_collection.count_documents({'method': 'PUT'})
    patch_results = nginx_collection.count_documents({'method': 'PATCH'})
    delete_results = nginx_collection.count_documents({'method': 'DELETE'})
    status_results = nginx_collection.count_documents({'path': '/status'})

    # get top IPs
    top_ips = nginx_collection.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'total': {'$sum': 1}
                }
        },
        {
            '$sort': {
                'total': -1
            }
        },
        {
            '$limit': 10
        }
    ])

    # print output
    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_results}")
    print(f"\tmethod POST: {post_results}")
    print(f"\tmethod PUT: {put_results}")
    print(f"\tmethod PATCH: {patch_results}")
    print(f"\tmethod DELETE: {delete_results}")
    print(f"{status_results} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['total']}")
