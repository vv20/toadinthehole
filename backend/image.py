import json
import os
import uuid

import boto3
from common import build_response_body, create_handler

s3 = boto3.resource('s3')

def get_presigned_url(event):
    image_id = str(uuid.uuid4())
    presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params = {
                'Bucket': os.environ['IMAGE_BUCKET_ARN'],
                'Key': image_id + '.jpg',
                'ContentType': 'image/jpeg',
                'ACL': 'public-read'
            })
    response = {
        'imageId': image_id,
        'presignedUrl': presigned_url,
    }
    return build_response_body(200, json.dumps(response), event)

handler = create_handler({
        'GET': get_presigned_url,
})
