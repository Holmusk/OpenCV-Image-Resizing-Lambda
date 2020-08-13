import boto3
import cv2
import os
import json
import numpy as np
#from io import BytesIO

s3 = boto3.resource('s3')


def opencv(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    objectKey = event['Records'][0]['s3']['object']['key']
    img_obj = s3.Object(
        bucket_name=bucketName,
        key=objectKey,
    )
    obj_body = img_obj.get()['Body'].read()

    try:
     
        img = cv2.imdecode(np.asarray(bytearray(obj_body)), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #Improve sharpness of image with unsharp masking.
        smoothed_image = cv2.GaussianBlur(img, (9, 9), 10)
        unsharped_masking = cv2.addWeighted(img, 1.5, smoothed_image, -0.5, 0)
        
        #improve image contrast
        # Improve contrast of image with contrast limited adaptive histogram equalization (CLAHE).
        clahe = cv2.createCLAHE(clipLimit=4.0)

        H, S, V = cv2.split(cv2.cvtColor(unsharped_masking, cv2.COLOR_RGB2HSV))
        eq_V = clahe.apply(V)
        eq_image = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2RGB)
        
        #add padding to image
        h, w = img.shape[:2]
        if h > w:
            diff = h-w
            pad_width = np.floor((diff)/2).astype(np.int)
            if (diff % 2) == 0:
                padded_image= np.pad(eq_image, ((0, 0), (pad_width, pad_width), (0, 0)),
                              'constant', constant_values=0)
            else:
                padded_image= np.pad(eq_image, ((0, 0), (pad_width, pad_width+1), (0, 0)),
                              'constant', constant_values=0)
        elif h < w:
            diff = w-h
            pad_width = np.floor((diff)/2).astype(np.int)
            if (diff % 2) == 0:
                padded_image=  np.pad(eq_image, ((pad_width, pad_width), (0, 0), (0, 0)),
                              'constant', constant_values=0)
            else:
                padded_image= np.pad(eq_image, ((pad_width, pad_width+1), (0, 0), (0, 0)),
                              'constant', constant_values=0)
        else:
            padded_image= eq_image
        dim = (512, 512)
        resized_img = cv2.resize(padded_image, dim, interpolation = cv2.INTER_CUBIC)
        #is_success,img_arr = cv2.imencode('.jpg',resized_img)
        #resized_imgbuffer = BytesIO(img_arr)
    except Exception as e:
        print(e)
        print('Error resizing file with OpenCV')
        raise e
    try:
        #resized_imgbuffer.seek(0)
        resized_imgobj = s3.Object(
        bucket_name=os.environ['OPENCV_OUTPUT_BUCKET'],
        #key=objectKey,
        key=objectKey.replace('.jpg', '.json')
        )
        resized_imgobj.put(
            Body=bytes(json.dumps({'channel_last': resized_img.tolist()}).encode('UTF-8')),
            ContentType='application/json')
        #resized_imgobj.put(Body=resized_imgbuffer, ContentType='image/jpeg')
    except Exception as e:
        print(e)
        print('Error uploading file to output bucket')
        raise e

