import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'Users')
table = dynamodb.Table(TABLE_NAME)

def get_http_method(event):
    # Support REST proxy and HTTP API v2 shapes
    m = event.get('httpMethod')
    if m:
        return m.upper()
    try:
        return event.get('requestContext', {}).get('http', {}).get('method', '').upper()
    except Exception:
        return None

def cors_response(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        method = get_http_method(event)
        # Respond to preflight OPTIONS
        if method == 'OPTIONS':
            return cors_response(200, {"message": "ok"})

        # Only allow GET for the actual operation
        # (you can relax/check auth if needed)
        if method and method != 'GET':
            return cors_response(405, {"message": "Method Not Allowed"})

        # Perform scan (ok for small datasets)
        resp = table.scan()
        items = resp.get('Items', [])
        users = []
        for it in items:
            users.append({
                'username': it.get('username'),
                'mobile': it.get('mobile'),
                'requirement': it.get('requirement'),
                'created_at': it.get('created_at')
            })

        return cors_response(200, {'users': users})
    except Exception as e:
        print("Error in get_users:", str(e))
        return cors_response(500, {'message': str(e)})
