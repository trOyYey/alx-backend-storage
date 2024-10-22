#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """
    function that changes all topics of a school document based on the name
    """
    mongo_collection.update_many(
        {"name": name},  # filter the documents to update
        {"$set": {"topics": topics}},  # update the topics field with the new topics
    )
