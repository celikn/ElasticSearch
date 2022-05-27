import PyPDF2
import re
import requests
import json
import os
from datetime import date
import random
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import datetime
import tqdm
import pdftotext

from faker import Faker



def generate_random_lonLat(num_rows):
    for _ in range(num_rows):
        hex1 = '%012x' % random.randrange(16**12) # 12 char random string
        flt = float(random.randint(0,100))
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        return [dec_lon,dec_lat]


def random_date():

    start =datetime.datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')

    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def deleteIndexMapping(indexName):
    client = Elasticsearch('http://localhost:9200')
    client.indices.delete(index=indexName)

def createIndexMapping(indexName):
    client = Elasticsearch('http://localhost:9200')

    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index=indexName,
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"},  
                    "content": {"type": "text"},  
                    "doc_type": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                }
            },
        },
    )
    return client


class ElasticModel:
    name = ""
    description = ""
    location=""
    content=""
    doc_type=""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)





def readPDF(path):
    with open(path, "rb") as f:
         pdf = pdftotext.PDF(f)
         line =" ".join(pdf)
         return line




#line = pageObj.extractText()

def prepareElasticDoc(pdfdir):
    listFiles = os.listdir(pdfdir)
    for file in listFiles :
            fake = Faker()
            path = pdfdir + "/" + file
            content = readPDF(path)
            doc = { 
                        "_id":random.randint(1,10000),
                        "name": file,
                        "author": fake.name(),
                        "content":content,
                        "doc_type": "pdf" or None,
                        "description":fake.sentence(),
                        "doc_date": random_date(),
                        "doc_path":path
                    }
            randomLatLon =generate_random_lonLat(1)
            lat = randomLatLon[1]
            lon = randomLatLon[0]
            if lat not in ("", "0") and lon not in ("", "0"):
                doc["location"] = {"lat": float(lat), "lon": float(lon)}
        
            yield doc


def main():
    indexName = "samplepdf"
    deleteIndexMapping(indexName)
    client=createIndexMapping(indexName)

    pdfdir = os.path.join( os.getcwd(),"ElasticSearchTest")
    listFiles = os.listdir(pdfdir)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=len(listFiles))
    successes = 0
    for ok, action in streaming_bulk(client=client, index=indexName, actions=prepareElasticDoc(pdfdir)):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, len(listFiles)))


if __name__ == "__main__":
        main()