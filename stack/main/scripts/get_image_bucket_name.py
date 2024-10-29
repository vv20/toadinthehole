
import sys

import boto3

from ..common import Component


def get_image_bucket_name(environment):
    client = boto3.client('s3')
    buckets = client.list_buckets(MaxResults=10)['Buckets']
    bucket = [b for b in buckets if Component.IMAGE_BUCKET.get_component_name(environment) in b['Name']][0]
    return bucket['Name']

if __name__ == '__main__':
    environment = sys.argv[1]
    print(get_image_bucket_name(environment))
