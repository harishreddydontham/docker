import boto3
import json 
import os
from dotenv import load_dotenv, find_dotenv 
from fastapi import FastAPI
import uvicorn
load_dotenv()

app1 = FastAPI()

@app1.get("/")
def homepage():
    return "you have reached home page of the fastapi application "

@app1.get("/getvpc")
def get_vpc_id_list(region):
    vpc_list=[]
    ec2 = boto3.client('ec2',region_name=region) 
    res = ec2.describe_vpcs().get('Vpcs')
    for vpc in res:
        vpc_list.append(vpc['VpcId'])
    print(vpc_list)
    return vpc_list

@app1.get("/s3")
def get_s3_buckets(region)->list:
    s3=boto3.client('s3', region_name=region) 
    res = s3.list_buckets()
    bucket_list = []
    for bucket in res['Buckets']:
        bucket_list.append(bucket['Name'])
    print(bucket_list)    
    return bucket_list    

@app1.get("/checks3")
def check_s3_buckets(bucket_name, region):
    s3=boto3.client('s3', region_name=region) 
    res = s3.list_buckets()
    bucket_list = []
    for bucket in res['Buckets']:
        bucket_list.append(bucket['Name'])
    if   bucket_name in bucket_list:
        return f"Bucket {bucket_name} exists . use a different name"  
    else:
        return f"Bucket {bucket_name} can be created"
    
@app1.get("/files")
def list_files_in_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_objects_v2(Bucket=bucket_name)
    file_list = []
    for obj in response['Contents']:
        file_list.append(obj['Key'])
    print(file_list)
    return file_list    

@app1.post("/upload")
def upload_file_to_bucket(bucket_name, file_path, region):
    s3 = boto3.client('s3', region_name=region)
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, file_name)
    return f"File {file_name} uploaded to bucket {bucket_name}"

    import mysql.connector

    