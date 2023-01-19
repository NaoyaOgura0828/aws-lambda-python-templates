import os
import json
import boto3
from decimal import Decimal


# DynamoDBのテーブルにアクセス
dynamodb_table_name = os.environ['DYNAMODB_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)


# Decimal型をJSONに変換するための関数
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


# Lambda関数のエントリーポイント
def lambda_handler(event, context):
    # 入力eventのログ出力処理
    print(event)

    statusCode = 200
    headers = {'Content-Type': 'application/json'}

    try:
        resource = event['resource']
        http_method = event['httpMethod']

        # 削除
        if (resource == '/items/{id}') and (http_method == 'DELETE'):
            id = event['pathParameters']['id']
            table.delete_item(Key={'id': id})
            body = f'id:{id}を削除しました。'

        # 一意検索
        elif (resource == '/items/{id}') and (http_method == 'GET'):
            id = event['pathParameters']['id']
            response = table.get_item(Key={'id': id})

            # Itemのみを表示する
            if 'Item' in response:
                body = response['Item']
            else:
                body = f'id:{id}は存在しません。'

        # 一覧
        elif (resource == '/items') and (http_method == 'GET'):
            response = table.scan()

            # Itemsを表示する
            if 'Items' in response:
                body = response['Items']
            else:
                body = f'Itemが存在しません。'

        # 登録
        elif (resource == '/items') and (http_method == 'PUT'):
            request = json.loads(event['body'])
            table.put_item(Item=request)
            body = f"id:{request['id']}を登録しました。"

        # 更新
        elif (resource == '/items/{id}') and (http_method == 'PUT'):
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
            print('失敗')
            raise ValueError(f'サポートされていないRouteKeyです: {resource}')

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
