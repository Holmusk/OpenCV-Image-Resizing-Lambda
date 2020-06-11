import boto3
import cv2
import os
import numpy as np
from io import BytesIO

s3 = boto3.resource('s3')


def opencv(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    bucketKey = event['Records'][0]['s3']['object']['key']
    img_obj = s3.Object(
        bucket_name=bucketName,
        key=bucketKey,
    )
    obj_body = img_obj.get()['Body'].read()

    try:
     
        img = cv2.imdecode(np.asarray(bytearray(obj_body)), cv2.IMREAD_COLOR)
        dim = (299, 299)
        resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
        is_success,img_arr = cv2.imencode('.jpg',resized_img)
        resized_imgbuffer = BytesIO(img_arr)
    except Exception as e:
        print(e)
        print('Error resizing file with OpenCV')
        raise e
    try:
        resized_imgbuffer.seek(0)
        resized_key="resized_{key}".format(key=bucketKey)
        resized_imgobj = s3.Object(
        bucket_name=os.environ['OPENCV_OUTPUT_BUCKET'],
        key=resized_key,
        )
        resized_imgobj.put(Body=resized_imgbuffer, ContentType='image/jpeg')
    except Exception as e:
        print(e)
        print('Error uploading file to output bucket')
        raise e

