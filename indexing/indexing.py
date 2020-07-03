from elasticsearch import Elasticsearch
import logging
import json
import codecs

def connect_elasticsearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Connected')
    else:
        print('failed to connect')   
    return es

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },

        "mappings": {
            "properties":{
            "songs": {
                "properties": {
                    "title": {
                        "type": "keyword"
                    },
                    "singer": {
                        "type": "keyword",
                        "store": True
                    },
                    "composer": {
                        "type": "keyword",
                        "store": True
                    },
                    "music": {
                        "type": "keyword",
                        "store": True
                    },
                    "lyrics": {
                        "type": "text"
                    },
                    "beat": {
                        "type": "keyword",
                        "store": True
                    },
                    "key": {
                        "type": "keyword",
                        "store": True
                    },
                    "gerne": {
                        "type": "text",
                        "store": True
                    },
                    "ratings": {
                        "type": "float",
                        "store": True
                    }
                }
            }}
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, body=settings)
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    return res


# read songs data
with codecs.open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/scraped_songs.json', 'r', encoding='utf-8') as json_file:
    text = json_file.read()
    data = json.loads(text)

# create index
es = connect_elasticsearch()
create_index(es, 'songs')

# add songs
for song in data:
	store_record(es, 'songs', song)









