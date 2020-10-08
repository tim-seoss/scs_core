#!/usr/bin/env python3

"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import os
import sys
from getpass import getpass

import boto3

from scs_core.aws.manager.s3_manager import S3Manager



def create_aws_client():
    env_key = "AWS_ACCESS_KEY_ID"
    env_secret_key = "AWS_SECRET_ACCESS_KEY"
    access_key_id = ""

    if env_key in os.environ:
        access_key_id = env_key
    if env_secret_key in os.environ:
        access_key_secret = env_secret_key

    else:
        print("No keys found in environment, please enter AWS Access Key: ", file=sys.stderr)
        access_key_id = input()
        print("Enter Secret AWS Access Key: ", file=sys.stderr)
        access_key_secret = getpass()

    if not access_key_id or not access_key_secret:
        exit(2)

    if access_key_id and access_key_secret:
        client = boto3.resource(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        client = boto3.resource('s3', region_name='us-west-2')

    return client


cwd = os.getcwd()
fp = cwd + "/bucket_file.txt"
print(fp)
exit()

boto_client = create_aws_client()
manager = S3Manager(boto_client)
# b = manager.list_buckets()
# print (b)
# d = manager.retrieve_from_bucket("scs-device-monitor", "MOCK_DATA.json")
# print (d)
cwd = os.getcwd()
fp = cwd + "/bucket_file.txt"
u = manager.upload_file_to_bucket("scs-device-monitor", fp, "testfile.txt")