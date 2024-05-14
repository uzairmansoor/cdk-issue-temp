import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    table_name = os.environ[f'TABLENAMETABLEONE']
    table_resource = dynamodb.Table(table_name)

    query_response = table_resource.query(
        KeyConditionExpression=Key('PartitionKey').eq('test'),
    )
    print(query_response)

    return json.dumps({"statusCode": 200, "body": "Hello from lambda"})

