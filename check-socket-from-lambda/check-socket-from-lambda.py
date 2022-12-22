import os
import socket
from urllib.parse import urlparse


def lambda_handler(event, context):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # タイムアウト設定(sec)
    str_set_time_out = os.environ['SET_TIME_OUT']
    set_time_out = int(str_set_time_out)
    sock.settimeout(set_time_out)

    host_dns_or_ip = os.environ['HOST_DNS_OR_IP']
    host = urlparse(host_dns_or_ip).netloc  # HOST_DNS_OR_IP を整形する

    # HOST_DNS_OR_IP の整形有無判定
    if host:
        pass
    else:
        host = host_dns_or_ip

    str_port = os.environ['PORT']
    port = int(str_port)  # PORT をstr⇒intに変換

    address = (host, port)

    # 実行処理
    try:
        ip_address = socket.gethostbyname(host)
        print("Host DNS or IP: " + host)
        print("Host IP: " + ip_address)
        print("接続試行中...")
        sock.connect(address)
        sock.shutdown(socket.SHUT_RDWR)
        print("接続成功！！！")
    except Exception as e:
        print("エラー")
        print(e)
    finally:
        sock.close()
