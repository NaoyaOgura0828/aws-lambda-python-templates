import os
import logging
from datetime import datetime

import boto3


def lambda_handler(event, context):

    # S3バケット名
    s3_bucket_name = os.environ['S3_BUCKET_NAME']

    # ファイル名
    file_name = 'test_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'

    # ファイル内容
    file_contents = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # ロギング設定
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    try:
        # ファイルを生成してS3へアップロードする
        s3 = boto3.resource('s3')
        object_file = s3.Object(s3_bucket_name, file_name)
        object_file.put(Body=file_contents)

        # 処理成功メッセージ
        response = (f'{s3_bucket_name}に{file_name}をアップロードしました。')

    # エラー処理
    except Exception as error:
        print('アップロードに失敗しました')
        logger.error(error)
        raise error

    else:
        # ログ出力
        print(response)

    # 処理成功メッセージの表示
    return response
