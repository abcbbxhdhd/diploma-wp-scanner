import json
import sys

import pymongo
from bson import ObjectId, json_util


def create_scan(scan_name, scan_url, scan_results):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['wp_scans_db']
    collection = db['scans_details']

    data = {
        "scan_name": scan_name,
        "scan_url": scan_url,
        "scan_results": scan_results
    }

    result = collection.insert_one(data)

    return result.inserted_id


def delete_scan(scan_id):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['wp_scans_db']
    collection = db['scans_details']

    result = collection.delete_one({'_id': ObjectId(scan_id)})

    return result.deleted_count


def get_scan_details(scan_id):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['wp_scans_db']
    collection = db['scans_details']

    if collection.count_documents({"_id": ObjectId(scan_id)}) == 0:
        return None

    return json.loads(json_util.dumps(collection.find_one({"_id": ObjectId(scan_id)})))


def get_all_scans():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['wp_scans_db']
    collection = db['scans_details']

    if collection.count_documents({}) == 0:
        return {}

    json_result = {}
    cursor = collection.find({})

    return json.loads(json_util.dumps(cursor))

