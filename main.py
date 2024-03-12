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
