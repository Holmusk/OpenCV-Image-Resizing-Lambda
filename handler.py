import boto3
import cv2
import numpy as np
import uuid
import os

s3Client = boto3.client('s3')


def opencv(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    bucketKey = event['Records'][0]['s3']['object']['key']

    download_path = '/tmp/{}{}'.format(uuid.uuid4(), bucketKey)
    output_path = '/tmp/{}'.format(bucketKey)

    s3Client.download_file(bucketName, bucketKey, download_path)

    try:
        img = cv2.imread(download_path)
        dim = (299, 299)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(output_path, resized)
    except Exception as e:
        print(e)
        print('Error resizing file with OpenCV')
        raise e
    try:
        s3Client.upload_file(output_path, os.environ['OPENCV_OUTPUT_BUCKET'], bucketKey)
    except Exception as e:
        print(e)
        print('Error uploading file to output bucket')
        raise e
    return bucketKey
