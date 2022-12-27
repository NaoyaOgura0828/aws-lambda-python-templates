import logging
import os

import boto3


def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    ec2 = boto3.client('ec2')
    ssm = boto3.client('ssm')
    instance_id = os.environ['INSTANCE_ID']
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    source_file_path = os.environ['SOURCE_FILE_PATH']
    target_file_path = os.environ['TARGET_FILE_PATH']

    try:
        # EC2のステータスを取得
        ec2_response = ec2.describe_instances(InstanceIds=[instance_id])
        ec2_state = ec2_response['Reservations'][0]['Instances'][0]['State']['Name']

        # EC2が起動しているか判定
        if not ec2_state == 'running':
            logger.error('EC2は起動していません。')
            return

        # S3バケット同期Command
        s3_sync_command = 'aws s3 sync s3://' + s3_bucket_name + \
            source_file_path + ' ' + target_file_path

        # Command実行
        ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunPowerShellScript',
            Parameters={
                'commands': [s3_sync_command],
                'executionTimeout': ['3600']
            },
        )
    # エラー処理
    except Exception as error:
        print('同期に失敗しました')
        logger.error(error)
        raise error
    else:
        print('同期に成功しました')
