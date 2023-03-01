# Always run when in backend folder, using command: python -m pytest api/tests 
import unittest
from unittest import mock
import json
import azure.functions as func
from  api import HttpTriggerCounter2
import logging
from azure.cosmos import CosmosClient

class TestFunction(unittest.TestCase):
    def test_counter2_function(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='../HttpTriggerCounter2',
            params=None)
        
        #construct a mock cosmo documentlist
        dct = {"id":"1", "visitcount" : 7}
        doc = func.Document.from_dict(dct)
        doc_list = func.DocumentList(initlist=[doc])

        # Call the function.
        resp = HttpTriggerCounter2.main(req, doc_list)

        with open('api/local.settings.json') as f:
            data = json.load(f)
            CONN_STR = data["Values"]["CosmosDBConnection"]
        
        #Read the update counter value from CosmosDB
        client = CosmosClient.from_connection_string(conn_str=CONN_STR)
        database_name = 'AzureResume'
        database = client.get_database_client(database_name)
        container_name = 'Counter'
        container = database.get_container_client(container_name)

        l=[]
        for item in container.query_items(query='SELECT * FROM container r WHERE r.id="1"', enable_cross_partition_query=True):
            l.append(item)

        # Check the output.
        self.assertEqual(
            l[0]["visitcount"],
            8,
        )
        