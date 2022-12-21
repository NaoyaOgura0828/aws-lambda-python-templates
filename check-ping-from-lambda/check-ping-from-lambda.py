import requests


def lambda_handler(event, context):
    response = requests.get('https://www.google.com/') # 接続先(IPアドレス, DNS, URL)

    print('ステータスコード: ' + str(response.status_code))
    print('-- レスポンス --')
    print(response.text)
    print('-- レスポンスここまで --')
