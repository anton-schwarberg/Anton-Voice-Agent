import json
import os
import secrets
import time
import boto3

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        eingabe = body.get("passwort", "")

        korrektes_passwort = os.environ["APP_PASSWORD"]
        ist_korrekt = (eingabe == korrektes_passwort)

        response = {
            "success": ist_korrekt
        }

        if ist_korrekt:
            token = secrets.token_hex(16)
            expires_at = int(time.time()) + 60

            response["token"] = token
            response["expiresAt"] = expires_at

            #DynamoDB speichern
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('TokenDB')
            table.put_item(Item={
                'token': token,
                'expiresAt': expires_at
            })
            print("Token erfolgreich in DynamoDB gespeichert.")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Content-Type": "application/json"
            },
            "body": json.dumps(response)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }