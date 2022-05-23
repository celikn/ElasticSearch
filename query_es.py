#!/usr/bin/env python3
#-*- coding: utf-8 -*-
##Source: https://kb.objectrocket.com/elasticsearch/how-to-query-elasticsearch-documents-in-python-268
from elasticsearch import Elasticsearch
import json, requests
import pprint
import pandas as pd
# create a client instance of Elasticsearch
elastic_client = Elasticsearch('http://localhost:9200')


index_name="nyc-restaurants"
# create a Python dictionary for the search query:
search_param = {
    "query": {
        "terms": {
            "_id": [ 1234, 42 ] # find Ids '1234' and '42'
        }
    }
}

# get a response from the cluster
response = elastic_client.search(index=index_name, body=search_param)
print ('response:', response)


some_string = '{"field1" : "fine me!"}'

# turn a JSON string into a dictionary:
some_dict = json.loads(some_string)

# Python dictionary object representing an Elasticsearch JSON query:
search_param = {
    'query': {
        'match': {
            'field1': 'find me!'
        }
    }
}

# get another response from the cluster
response = elastic_client.search(index=index_name, body=search_param)
print (response.to_dict())
with open('response.json', 'w') as out:
    out.write(json.dumps(response.to_dict()))