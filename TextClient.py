import json

import boto3 as boto3


def send_message():
    payload3 = b"""{
    "destinationNumber": "4702637816",
    "firstName": "Austin",
    "lastName": "Miles",
    "source": "Subscribe?"
    }"""
    client = get_boto3_client()
    client.invoke(
        FunctionName="CanvasText",
        InvocationType="Event",
        Payload=payload3
    )


def get_boto3_client():
    with open('aws-creds.json') as f:
        creds = json.load(f)
    access_key = creds['access_key']
    secret = creds['secret_key']
    client = boto3.client(
        'lambda',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        region_name='us-east-1'
    )
    return client


if __name__ == '__main__':
    send_message()
