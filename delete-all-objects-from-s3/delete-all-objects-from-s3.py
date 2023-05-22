import os
import logging

import boto3


def lambda_handler(event, context):

    # S3バケット名
    s3_bucket_name = os.environ['S3_BUCKET_NAME']

    # ロギング設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        # S3からファイルの内容を取得する
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=s3_bucket_name)

        # S3バケットにオブジェクトがあるか確認
        if 'Contents' in response:
            # オブジェクトリスト作成
            objects_list = [{'Key': obj['Key']}
                            for obj in response['Contents']]

            # オブジェクト削除
            s3.delete_objects(Bucket=s3_bucket_name, Delete={
                              'Objects': objects_list})

            logger.info('S3バケットのすべてのオブジェクトが削除されました。')

        else:
            logger.info('S3バケットは既に空です。')

    # エラー処理
    except Exception as error:
        logger.error('オブジェクトの削除に失敗しました。')
        logger.error(error)
        raise error

    # 正常終了
    return {
        'statusCode': 200,
        'body': '正常終了'
    }
