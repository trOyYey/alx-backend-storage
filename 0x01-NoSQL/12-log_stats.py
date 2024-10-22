#!/usr/bin/env python3
""" 12-log_stats """
from pymongo import MongoClient


def main():
    """
    Python script that provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    get = logs_collection.count_documents({'method': 'GET'})
    post = logs_collection.count_documents({'method': 'POST'})
    put = logs_collection.count_documents({'method': 'PUT'})
    patch = logs_collection.count_documents({'method': 'PATCH'})
    delete = logs_collection.count_documents({'method': 'DELETE'})
    st = logs_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{logs_collection.count_documents({})} logs')
    print('Methods:')
    print(f'\tmethod GET: {get}'.format(get))
    print(f'\tmethod POST: {post}'.format(post))
    print(f'\tmethod PUT: {put}'.format(put))
    print(f'\tmethod PATCH: {patch}'.format(patch))
    print(f'\tmethod DELETE: {delete}'.format(delete))
    print(f'{st} status check'.format(st))


if __name__ == "__main__":
    main()
