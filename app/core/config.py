import boto3
from botocore.exceptions import NoCredentialsError
import os

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
REGION_NAME = 'ap-south-2'  

s3 = boto3.client('s3', 
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,
                  region_name=REGION_NAME) 

def upload_to_s3(file, filename):
    try:
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False