import os
import json
import boto3
import hashlib
import binascii
import datetime
import base64

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'Users')
table = dynamodb.Table(TABLE_NAME)

# Cache the table primary key name (partition key)
def get_partition_key_name():
    try:
        resp = dynamodb_client.describe_table(TableName=TABLE_NAME)
        ks = resp['Table']['KeySchema']
        # find HASH key (partition)
        for entry in ks:
            if entry.get('KeyType') == 'HASH':
                return entry.get('AttributeName')
    except Exception as e:
        print("Error getting key schema:", str(e))
    # fallback
    return 'username'

PARTITION_KEY = get_partition_key_name()

def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return binascii.hexlify(dk).decode(), binascii.hexlify(salt).decode()

def get_http_method(event):
    m = event.get('httpMethod')
    if m:
        return m.upper()
    try:
        return event.get('requestContext', {}).get('http', {}).get('method', '').upper()
    except Exception:
        return None

def lambda_handler(event, context):
    try:
        method = get_http_method(event)
        if method == 'OPTIONS':
            return cors_response(200, "")

        body = event.get('body')
        if body is None:
            data = {}
        else:
            if isinstance(body, str):
                if event.get('isBase64Encoded'):
                    body = base64.b64decode(body).decode('utf-8')
                try:
                    data = json.loads(body) if body else {}
                except json.JSONDecodeError:
                    data = {}
            elif isinstance(body, dict):
                data = body
            else:
                data = {}

        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        mobile = data.get('mobile') or ''
        requirement = data.get('requirement') or ''

        if not username or not password:
            return cors_response(400, {"message":"username and password are required"})

        pwd_hash, salt = hash_password(password)

        # Build the item using the actual partition key name
        item = {
            PARTITION_KEY: username,
            'password_hash': pwd_hash,
            'salt': salt,
            'mobile': mobile,
            'requirement': requirement,
            'created_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }

        table.put_item(Item=item)
        return cors_response(201, {"message":"user saved"})
    except Exception as e:
        print("Error in save_user:", str(e))
        return cors_response(500, {"message": str(e)})

def cors_response(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(body)
    }
