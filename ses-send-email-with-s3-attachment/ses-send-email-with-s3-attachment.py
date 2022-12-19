import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def lambda_handler(event, context):
    """ 各種設定 """

    # 送信元メールアドレス
    sender = '送信元メールアドレス'

    # 送信先メールアドレス
    recipient = '送信先メールアドレス'

    # ConfigurationSetの指定。
    # ConfigurationSetを使用しない場合は、以下の変数と引数をコメントアウトする。。
    # 変数: configuration_set = 'ConfigSet'
    # 引数: ConfigurationSetName=configuration_set
    # configuration_set = 'コンフィグセット'

    # SES構築リージョン
    aws_region = 'ap-northeast-1'

    # Eメールの文字エンコーディング。
    charset = 'utf-8'

    # S3バケット名
    s3_bucket_name = 'バケット名'

    # 添付ファイル名
    attachment_file_name = '添付ファイル名'

    # 添付ファイルを格納するLambda内のファイルパス
    attachment_file_path = '/tmp/' + attachment_file_name

    # メールの件名
    subject = '添付メールの実験'

    # HTML以外のメールクライアントを持つ受信者のためのメール本文
    body_text = '添付メールの実験,\r\n添付ファイルはありますか？'

    # メールのHTML本文
    body_html = """\
    <html>
    <head></head>
    <body>
    <h1>添付メールの実験</h1>
    <p>添付ファイルはありますか？</p>
    </body>
    </html>
    """

    """"""

    # 新しいSESリソースを作成し、地域を指定する。
    client = boto3.client('ses', region_name=aws_region)

    # multipart/mixedの親コンテナを作成する。
    message = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # multipart/alternative の子コンテナを作成する。
    message_body = MIMEMultipart('alternative')

    # テキストとHTMLコンテンツをエンコードし、文字エンコーディングを設定する。
    # ASCIIの範囲外の文字を含むメッセージを送信する場合に必要。
    textpart = MIMEText(body_text.encode(charset), 'plain', charset)
    htmlpart = MIMEText(body_html.encode(charset), 'html', charset)

    # テキスト部分とHTML部分を子コンテナに追加する。
    message_body.attach(textpart)
    message_body.attach(htmlpart)

    # 添付ファイルをS3からダウンロードする。
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket_name)
    bucket.download_file(attachment_file_name, attachment_file_path)

    # 添付ファイル部分を定義し、MIMEApplicationを使用してエンコードする。
    attachment_file = MIMEApplication(open(attachment_file_path, 'rb').read())

    # この部分を添付ファイルとして扱うようにメールクライアントに伝えるヘッダを追加。
    # そして、添付ファイルに名前を付ける。
    attachment_file.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(attachment_file_path))

    # multipart/alternative の子コンテナを multipart/mixed にアタッチする。
    # 親コンテナにアタッチする。
    message.attach(message_body)

    # 親コンテナに添付ファイルを追加する。
    message.attach(attachment_file)
    # print(message)
    try:
        # メールを送信する
        response = client.send_raw_email(
            Source=sender,
            Destinations=[
                recipient
            ],
            RawMessage={
                'Data': message.as_string(),
            },
            # ConfigurationSetName=configuration_set
        )
    # エラー処理
    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        print('Email sent! Message ID:'),
        print(response['ResponseMetadata']['RequestId'])


# main function
if __name__ == '__main__':
    lambda_handler({}, {})
