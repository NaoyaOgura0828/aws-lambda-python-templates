import os
import logging

import boto3


def lambda_handler(event, context):
    # S3バケット名
    s3_bucket_name = os.environ['S3_BUCKET_NAME']

    # ファイル名
    file_name = os.environ['FILE_NAME']

    # ロギング設定
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    try:
        # S3からファイルの内容を取得する
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=s3_bucket_name, Key=file_name)
        file_contents = response['Body'].read()
        # file_contentsのdecode
        decoded_file_contents = file_contents.decode()

        # 処理成功メッセージ
        response = (f'{s3_bucket_name}から{file_name}をダウンロードしました。')

    # エラー処理
    except Exception as error:
        print('ダウンロードに失敗しました')
        logger.error(error)
        raise error

    else:
        # ログ出力
        print(response)
        print('-- ファイル内容 --')
        print(decoded_file_contents)
        print('-- ファイル内容ここまで --')

    # 処理成功メッセージの表示
    return response
