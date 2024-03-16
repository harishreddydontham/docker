import boto3
import json 
import os
from dotenv import load_dotenv, find_dotenv 
from fastapi import FastAPI
import uvicorn
import mysql.connector
load_dotenv()

app1 = FastAPI()
con_name = os.getenv("HOSTNAME")
python_version = os.getenv("PYTHON_VERSION")
@app1.get("/")
def homepage():
    return f'your api is processed by the container with ID {con_name} running python version {python_version}.'

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


@app1.get("/connect_mysql")
def connect_mysql(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            return "Connected to MySQL database"
        else:
            return "Failed to connect to MySQL database"
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"


@app1.get("/create_table")
def create_table(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            # Create table query
            create_table_query = """
            CREATE TABLE customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                location VARCHAR(255),
                email VARCHAR(255)
            )
            """
            # Execute the create table query
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
            return "Table 'customers' created successfully"
        else:
            return "Failed to connect to MySQL database"
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"
    
@app1.get("/insert_data")
def insert_data(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            # Insert data query
            insert_data_query = """
            INSERT INTO customers (name, location, email) VALUES
            ('John', 'USA', 'john@gmal.com'),
            ('Alex', 'UK', 'alex@gmail.com'),
            ('Sue', 'Canada', 'sue@gmail.com');
            """
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"
    


    