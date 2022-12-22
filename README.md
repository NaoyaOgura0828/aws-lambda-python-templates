# aws-lambda-python-collection
AWS Lambdaで動作するPythonコード集

<br>

# Tree
本リポジトリは以下のファイル構成である。

```bash
aws-lambda-python-collection
├── README.md
├── check-requests-from-lambda # LambdaからHTTPまたはHTTPSリクエストをする
│   ├── LambdaLayer.zip # LambdaLayer用zip
│   ├── check-requests-from-lambda.py
│   └── create_lambda_layer_for_python_requests.sh # LambdaLayer.zip作成スクリプト
├── check-socket-from-lambda # Lambdaからの疎通を確認する
│   └── check-socket-from-lambda.py
├── images
│   ├── check-requests-from-lambda.png # 環境変数イメージ
│   └── check-socket-from-lambda.png # 環境変数イメージ
└── ses-send-email-with-s3-attachment # SESでS3に配置されたファイルを添付送信する
    └── ses-send-email-with-s3-attachment.py
```

<br>

# Requirement
AWS Lambdaでの動作を前提とする。<br>
Lambdaには、動作に必要な権限が付与されたIAMロールがアタッチされている事。

<br>

# Usage
## check-requests-from-lambda
- `create_lambda_layer_for_python_requests.sh`を実行する。<br>
このスクリプトは`LambdaLayer.zip`を生成する。<br>
RockyLinux9.1環境で動作確認済
- AWS Lambdaのレイヤーを作成する。<br>
生成した`LambdaLayer.zip`をアップロードする。
- Lambda関数を作成する。
- 環境変数に以下の項目を設定する。

<img src='images/check-requests-from-lambda.png'>

```conf
HOST_DNS_OR_IP = ${HostのDNSまたはIP}
SET_TIME_OUT = ${タイムアウトするまでの秒数}
```

<br>

## check-socket-from-lambda
- Lambda関数を作成する。
- 環境変数に以下の項目を設定する。

<img src='images/check-socket-from-lambda.png'>

```conf
HOST_DNS_OR_IP = ${HostのDNSまたはIP}
PORT = ${接続ポート}
SET_TIME_OUT = ${タイムアウトするまでの秒数}
```

<br>

## ses-send-email-with-s3-attachment
- Lambda関数を作成する。
- SESに`検証済み ID`を設定する。`設定セット`を利用する場合は、`設定セット`を設定する。
- `${添付ファイル名}`と一致するファイルを`${バケット名}`と一致するS3バケットに配置する。
- 以下の項目を設定する事。

```python
    """ 各種設定 """

    # 送信元メールアドレス
    sender = '${送信元メールアドレス}'

    # 送信先メールアドレス
    recipient = '${送信先メールアドレス}'

    # 設定セットの指定。
    # 設定セットを使用しない場合は、以下の変数と引数をコメントアウトする。。
    # 変数: configuration_set = '${設定セット名}'
    # 引数: ConfigurationSetName=configuration_set
    configuration_set = '${設定セット名}'

    # SES構築リージョン
    aws_region = '${リージョン}'

    # Eメールの文字エンコーディング。
    charset = '${文字コード}'

    # S3バケット名
    s3_bucket_name = '${バケット名}'

    # 添付ファイル名
    attachment_file_name = '${添付ファイル名}'

    # メールの件名
    subject = '${メールの件名}'

    # HTML以外のメールクライアントを持つ受信者のためのメール本文
    body_text = '${メールの本文 1},\r\n${メールの本文 2}'

    # メールのHTML本文
    body_html = """\
    <html>
    <head></head>
    <body>
    <h1>${メールの本文 1}</h1>
    <p>${メールの本文 2}</p>
    </body>
    </html>
    """

    """"""
```

<br>
