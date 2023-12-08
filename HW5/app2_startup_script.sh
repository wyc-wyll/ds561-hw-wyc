#! /bin/bash

echo "setting up"

sudo apt-get update
sudo apt-get -y install python3 python3-pip

gsutil cp gs://ds561-bucket/http-client.py /http-client.py