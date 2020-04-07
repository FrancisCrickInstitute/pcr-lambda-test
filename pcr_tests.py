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
        df = pd.read_csv(download_path, usecols=[0, 7, 14, 16, 21], names=[
            "Well Position", "CT", "R(superscript 2)", "Efficiency", "Baseline End"], header=0)

        # when Efficiency  value > 90% and < 110%  > set Efficiency Pass to true - this seems to work
        mask = (df['Efficiency'] > 89) & (df['Efficiency'] < 110) | False
        df['Efficiency Pass'] = mask

        # when R2 value > 0.95 > set R2 Pass to true
        mask = (df['R(superscript 2)'] >= 0.95) | False
        df['R2 Pass'] = mask

        # when CT > Baseline end and < 37 set CT Pass to true
        mask = (df['CT'] > df['Baseline End']) & (df['CT'] < 38) | False
        df['CT Pass'] = mask

        csv_buf = StringIO()
        df.to_csv(csv_buf, header=None, index=False, encoding='utf-8')
        csv_buf.seek(0)
        s3_client.put_object(Bucket='fci-poc-outgoing-data',
                             Body=csv_buf.getvalue(), Key=tmpkey)
        if os.path.exists(download_path):
            os.remove(download_path)
            print("Removed the file %s" % download_path)
        else:
            print("Sorry, file %s does not exist." % download_path)
