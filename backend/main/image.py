import math
import os

import boto3
import cv2
from cv2.typing import MatLike

from .common import build_response_body, create_handler

s3 = boto3.client('s3')

def standardise_image(event):
    if not 'queryStringParameters' in event or event['queryStringParameters'] is None or not 'imadeID' in event['queryStringParameters']:
        return build_response_body(400, 'Missing image ID', event)

    image_id: str = event['queryStringParameters']['imageID']
    input_image_path: str = '/tmp/' + image_id + '.jpg'
    output_image_path: str = '/tmp/' + image_id + '-processed.jpg'
    target_height: int = int(os.environ['IMAGE_HEIGHT'])
    target_width: int = int(os.environ['IMAGE_WIDTH'])
    target_ar: float = target_height / target_width

    # retrieve the image from S3
    s3.download_file(
        Bucket=os.environ['IMAGE_BUCKET_NAME'],
        Key=image_id + '.jpg',
        Filename=input_image_path)
    img: MatLike = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
    
    # crop to correct aspect ratio
    img_height: int = img.shape[0]
    img_width: int = img.shape[1]
    img_ar: float = img_height / img_width
    if img_ar > target_ar: # crop height
        excess_height = img_height - math.floor(img_width * target_ar)
        height_margin = math.floor(excess_height / 2)
        img = img[height_margin:img_height - height_margin, :]
    elif img_ar < target_ar: # crop width
        excess_width = img_width - math.floor(img_height / target_ar)
        width_margin = math.floor(excess_width / 2)
        img = img[:, width_margin:img_width - width_margin]
    # otherwise the aspect ratio is spot on

    # resize
    img = cv2.resize(img, (target_width, target_height), interpolation = cv2.INTER_AREA)

    # save
    cv2.imwrite(output_image_path, img)

    # upload the image back to S3
    s3.upload_file(
        Bucket=os.environ['IMAGE_BUCKET_NAME'],
        Key=image_id + '.jpg',
        Filename=output_image_path)

handler = create_handler({
        'POST': standardise_image,
})
