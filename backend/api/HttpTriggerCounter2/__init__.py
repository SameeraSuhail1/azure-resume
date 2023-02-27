"""import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )"""


import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

def main(req: func.HttpRequest, azureresume: func.DocumentList) -> str:
    if not azureresume:
        logging.warning("azureresume not found")
    else:
        logging.info("Found azureresume, Description=%s",
                     azureresume[0]['visitcount'])
        
        current_count = azureresume[0]['visitcount']
        updated_count = azureresume[0]['visitcount'] +1


         
    CONN_STR = os.environ['CosmosDBConnection']
    #CONN_STR = "AccountEndpoint=https://azure-resume-nosql.documents.azure.com:443/;AccountKey=sWp3MWftphK90KqlM8QlJM1ahQQS9efZBPvQDdXltbeorKKIVhdBpbr1DfJYXUVyEf5c3JCZpMiDACDb8B0jLQ==;"
    client = CosmosClient.from_connection_string(conn_str=CONN_STR)
    database_name = 'AzureResume'
    database = client.get_database_client(database_name)
    container_name = 'Counter'
    container = database.get_container_client(container_name)

    container.upsert_item({
            'id': '1',
            'visitcount': updated_count
        }
    )
    return str(current_count)