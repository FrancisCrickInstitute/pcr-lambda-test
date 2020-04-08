import json
import boto3
import pandas as pd
from io import StringIO

import os
import sys
import uuid
from urllib.parse import unquote_plus

outputPath = 's3://fci-poc-outgoing-data/'
csvPath = 's3://fci-working-data/'
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/'+tmpkey
        s3_client.download_file(bucket, key, download_path)
        sheets = ['Results', 'Amplification Data']
        data_xls = pd.read_excel(
            download_path, sheets, index_col=0, skiprows=40,  header=0)
        df = pd.DataFrame()
        for sheet in sheets:
            df = df.append(data_xls[sheet], ignore_index=True, sort=False)
        csv_buf = StringIO()
        df.to_csv(csv_buf, header=None, index=False, encoding='utf-8')
        csv_buf.seek(0)
        s3_client.put_object(Bucket='fci-working-data',
                             Body=csv_buf.getvalue(), Key=os.path.splitext(tmpkey)[0]+'.csv')

        if os.path.exists(download_path):
            os.remove(download_path)
            print("Removed the file %s" % download_path)
        else:
            print("Sorry, file %s does not exist." % download_path)
