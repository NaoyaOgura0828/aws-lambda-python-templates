import os
import re

import requests
from requests.exceptions import RequestException


def lambda_handler(event, context):
    # タイムアウト設定(sec)
    str_set_time_out = os.environ['SET_TIME_OUT']
    set_time_out = int(str_set_time_out)

    pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    host_dns_or_ip = os.environ['HOST_DNS_OR_IP']

    # host_dns_or_ip 整形
    if re.match(pattern, host_dns_or_ip):
        pass
    else:
        host_dns_or_ip = 'http://' + host_dns_or_ip

    # 実行処理
    try:
        response = requests.get(host_dns_or_ip, timeout=set_time_out)
        print('接続に成功しました')
        print('ステータスコード: ' + str(response.status_code))
        print('-- レスポンス --')
        print(response.text)
        print('-- レスポンスここまで --')
    except RequestException as error:
        print('接続に失敗しました')
        print(error)
