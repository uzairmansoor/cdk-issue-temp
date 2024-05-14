import json
import boto3
import os

def handler(event, context):
    table_names = os.environ['TABLE_NAMES'].split(',')
    resource_ids = [f"arn:aws:dynamodb:{os.environ['AWS_REGION']}:{os.environ['AWS_ACCOUNT_ID']}:table/{table_name}" for table_name in table_names]

    if event['detail']['eventName'] in ['DeleteStack', 'DeleteResource']:
        client = boto3.client('dynamodb')
        for table_id in resource_ids:
            try:
                client.delete_table(TableName=table_id.split('/')[-1])
                print(f"Table {table_id} deleted successfully.")
            except client.exceptions.ResourceNotFoundException:
                print(f"Table {table_id} not found.")
            except Exception as e:
                print(f"Error deleting table {table_id}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Tables deleted successfully!')
    }
