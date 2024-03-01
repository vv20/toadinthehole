import boto3
import os
import uuid

from common import build_response_body

s3 = boto3.resource('s3')

def save_image(event):
    image_id     = str(uuid.uuid5())
    image_object = s3.Object(os.environ['image_bucket_name'], image_id)
    return build_response_body(201, image_id)

methodDict = {
        'PUT': save_image,
}

def handler(event, context):
    if event['httpMethod'] not in methodDict:
        return build_response_body(400, "HTTP method not supported")
    try:
        return methodDict[event['httpMethod']](event)
    except:
        return build_response_body(500, "Internal Server Error")
