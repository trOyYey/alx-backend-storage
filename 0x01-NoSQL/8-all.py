#!/usr/bin/env python3
""" task-8 """


def list_all(mongo_collection):
    """
    List all documents in Python
    """
    return mongo_collection.find({})
