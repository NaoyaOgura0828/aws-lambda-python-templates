import os
import logging
import time

import boto3


def lambda_handler(event, context):

    # CloudFront ディストリビューションID
    distribution_id = os.environ['CLOUDFRONT_DISTRIBUTION_ID']

    # ロギング設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        # キャッシュ削除
        cloudfront = boto3.client('cloudfront')
        cloudfront.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': ['/*']
                },
                'CallerReference': str(time.time())
            }
        )

        logger.info('キャッシュの削除に成功しました。')

    except Exception as error:
        logger.error('キャッシュの削除に失敗しました。')
        logger.error(error)
        raise error

    # 正常終了
    return {
        'statusCode': 200,
        'body': '正常終了'
    }
