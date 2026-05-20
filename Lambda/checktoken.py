import json
import os
import boto3
import time

dynamodb = boto3.resource('dynamodb').Table('TokenDB')
WEBHOOK_URL = os.environ["MAKE_WEBHOOK_URL"]

def lambda_handler(event, context):
    token = json.loads(event.get("body", "{}")).get("token")
    item = dynamodb.get_item(Key={'token': token}).get("Item")

    if item and int(item["expiresAt"]) > int(time.time()):
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({ "webhook": WEBHOOK_URL })
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps("false")
    }