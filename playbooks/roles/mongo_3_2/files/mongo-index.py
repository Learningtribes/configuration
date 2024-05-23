import pymongo
import sys
import urllib
from pymongo import MongoClient


username = urllib.quote_plus(sys.argv[1])
password = urllib.quote_plus(sys.argv[2])

client = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))

db_edxapp = client['edxapp']
collection_mav = db_edxapp['modulestore.active_versions']
collection_mav.create_index(
    [("org", pymongo.ASCENDING), 
    ("run", pymongo.ASCENDING), 
    ("course", pymongo.ASCENDING)], 
    backgroud=True)
collection_fc = db_edxapp['fs.chunks']
collection_fc.create_index([("files_id". pymongo.ASCENDING)], backgroud=True)

db_ccs = client['cs_comments_service']
collection_contents = db_ccs['contents']
collection_contents.create_index(
    [("author_id", pymongo.ASCENDING),
    ("course_id", pymongo.ASCENDING),
    ("anonymous", pymongo.ASCENDING),
    ("anonymous_to_peers", pymongo.ASCENDING),
    ("_type", pymongo.ASCENDING)],
    backgroud=True)
collection_contents.create_index(
    [("_id", pymongo.ASCENDING), 
    ("_type", pymongo.ASCENDING)], 
    backgroud=True)
collection_contents.create_index(
    [("_type", pymongo.ASCENDING),
    ("commentable_id", pymongo.ASCENDING),
    ("course_id", pymongo.ASCENDING),
    ("context", pymongo.ASCENDING)],
    backgroud=True)
collection_contents.create_index(
    [("_type", pymongo.ASCENDING),
    ("commentable_id", pymongo.ASCENDING),
    ("course_id", pymongo.ASCENDING),
    ("group_id", pymongo.ASCENDING)],
    backgroud=True)
collection_contents.create_index(
    [("created_at", pymongo.ASCENDING),
    ("comment_thread_id", pymongo.ASCENDING),
    ("_type", pymongo.ASCENDING)],
    backgroud=True)
collection_contents.create_index([("votes.up", pymongo.ASCENDING)], backgroud=True)
collection_contents.create_index([("votes.down", pymongo.ASCENDING)], backgroud=True)
collection_contents.create_index([("_type", pymongo.ASCENDING)], backgroud=True)
collection_users = db_ccs['users']
collection_users.create_index([("external_id", pymongo.ASCENDING)], backgroud=True)
collection_users.create_index([("username", pymongo.ASCENDING)], backgroud=True)
collection_subscriptions = db_ccs['subscriptions']
collection_subscriptions.create_index(
    [("subscriber_id", pymongo.ASCENDING),
    ("source_type", pymongo.ASCENDING)],
    backgroud=True)