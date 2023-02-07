import os
import logging

import psycopg2


def lambda_handler(event, context):

    # ServerDNS or ServerIP
    server_dns_or_ip = os.environ['SERVER_DNS_OR_IP']

    # DB名
    db_name = os.environ['DB_NAME']

    # テーブル名
    table_name = os.environ['TABLE_NAME']

    # DBユーザー名
    db_user_name = os.environ['DB_USER_NAME']

    # DBユーザーパスワード
    db_user_password = os.environ['DB_USER_PASSWORD']

    # DB接続設定
    db_connection = psycopg2.connect(host=server_dns_or_ip,
                                     database=db_name,
                                     user=db_user_name,
                                     password=db_user_password)

    # SQL
    sql = (f'INSERT INTO {table_name} (id, name, age) VALUES (%s, %s, %s)')

    # ロギング設定
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # 空のvalues_listを定義
    values_list = []

    try:
        for keys in event:

            # Key別Value取り出し
            id = keys['id']
            name = keys['name']
            age = keys['age']

            # separate_values_listへ格納
            separate_values_list = [id, name, age]

            # separate_values_listをvalues_listへ追加
            values_list.append(separate_values_list)

        # DB接続
        with db_connection:
            with db_connection.cursor() as cursor:
                # SQL実行
                cursor.executemany(sql, values_list)

            # コミットしてトランザクション実行
            db_connection.commit()

        # 処理成功メッセージ
        response = (f'DB名:{db_name} テーブル名:{table_name} に書き込みが完了しました。')

    except Exception as error:
        print('処理に失敗しました')
        logger.error(error)
        raise error

    else:
        # ログ出力
        print(response)

    # 処理成功メッセージの表示
    return response
