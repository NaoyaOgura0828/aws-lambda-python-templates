import os
import json
import boto3
from decimal import Decimal


# DynamoDBのテーブルにアクセス
dynamodb_table_name = os.environ['DYNAMODB_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)


# Decimal型をJSONに変換する
def json_serialize(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


# update_itemに必要なparameterを整形する
def get_update_params(request):
    update_expression = ['set ']
    update_values = dict()

    for key, value in request.items():
        update_expression.append(f' {key} = :{key},')
        update_values[f':{key}'] = value

    return ''.join(update_expression)[:-1], update_values


def lambda_handler(event, context):
    # 入力eventのログ出力処理
    print(event)

    statusCode = 200
    headers = {'Content-Type': 'application/json'}

    try:
        route_key = event['routeKey']

        # 削除
        if route_key == 'DELETE /items/{id}':
            id = event['pathParameters']['id']
            table.delete_item(Key={'id': id})
            body = f'id:{id}を削除しました。'

        # 一意検索
        elif route_key == 'GET /items/{id}':
            id = event['pathParameters']['id']
            response = table.get_item(Key={'id': id})

            # Itemのみを表示する
            if 'Item' in response:
                body = response['Item']
            else:
                body = f'id:{id}は存在しません。'

        # 一覧
        elif route_key == 'GET /items':
            response = table.scan()
            body = response['Items']

        # 登録
        elif route_key == 'PUT /items':
            request = json.loads(event['body'])
            table.put_item(Item=request)
            body = f"id:{request['id']}を登録しました。"

        # 更新
        elif route_key == 'PUT /items/{id}':
            request = json.loads(event['body'])
            id = event['pathParameters']['id']
            key, value = get_update_params(request)

            table.update_item(
                Key={'id': id},
                UpdateExpression=key,
                ExpressionAttributeValues=dict(value)
            )

            body = f'id:{id}を更新しました。'

        else:
            raise ValueError(f'サポートされていないRouteKeyです: {route_key}')

    except Exception as error:
        statusCode = 400
        body = error

    finally:
        # jsonを整形して出力
        body = json.dumps(body, default=json_serialize,
                          ensure_ascii=False, indent=2)

    return {
        'statusCode': statusCode,
        'body': body,
        'headers': headers
    }
