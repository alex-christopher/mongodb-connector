import pymongo
from pymongo.mongo_client import MongoClient
import pandas as pd
import numpy as np
import json

class MongodbConnector:
    __collection = None
    __database = None


    def __init__(self, url_link : str, database_name : str, collection_name : None):
        self.url_link = url_link
        self.database_name = database_name
        self.collection_name = collection_name

    def url_link(self):
        client = MongoClient(self.url_link)
        
        return client

    def create_database(self):
        if MongodbConnector.__database==None:
            client = self.url_link()
            self.database = client[self.database_name]
        
        return self.database

    def create_collection(self, collection = None):
        if MongodbConnector.__collection == None:
            database = self.create_database()
            self.collection = database[self.collection_name]
            MongodbConnector.__collection = self.collection

        if MongodbConnector.__collection != None:
            database = self.create_database()
            self.collection = database[self.collection_name]
            MongodbConnector.__collection = self.collection
        
        return self.collection

    def insert_data(self, data : str, collection_name : str):
        if type(data) == list:
            for i in data:
                if type(data) != dict:
                    raise TypeError("Data must be in dictionary format")
            collection = self.create_collection(collection_name)
            collection.insert_many(data)
        
        elif type(data) == dict:
            collection = self.create_collection(collection)
            collection.insert_one(data)

    def bulk_insert(self, datafile, collection_name : None):
        self.path = datafile

        if self.path.endswith(".csv"):
            dataframe = pd.read_csv(self.path, encoding="utf-8")
        
        elif self.path.endswith("xlsx"):
            dataframe = pd.read_excel(self.path, encoding="utf-8")

        datajson = json.loads(dataframe.to_json(orient="records"))
        collection = self.create_collection()
        collection.insert_many(datajson)
