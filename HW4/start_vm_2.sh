#! /bin/bash

echo "setting up"

sudo apt-get update
sudo apt-get -y install python3 python3-pip

gsutil cp gs://hw2-ds561/http-client.py /http-client.py


