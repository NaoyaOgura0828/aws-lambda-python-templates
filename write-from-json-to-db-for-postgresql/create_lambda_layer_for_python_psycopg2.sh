#!/bin/bash

# python ディレクトリ作成
mkdir python/
cd python/

# Install gcc
sudo dnf install gcc -y

# Install gcc-c++
sudo dnf gcc-c++ -y

# Install kernel-devel
sudo dnf kernel-devel -y

# Install python3-devel
sudo dnf python3-devel -y

# Install libxslt-devel
sudo dnf libxslt-devel -y

# Install libffi-devel
sudo dnf libffi-devel -y

# Install openssl-devel
sudo dnf openssl-devel -y

# Install python3-pip
sudo dnf install python3-pip -y

# Install zip
sudo dnf install zip -y

# Upgrade pip
pip3 install --upgrade pip

# Install psycopg2
pip3 install -t ./ psycopg2-binary

# LambdaLayer.zip 作成
cd ..
zip -r LambdaLayer.zip python/

# python ディレクトリ削除
rm -drf python

exit 0