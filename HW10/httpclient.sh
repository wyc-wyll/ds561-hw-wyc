#! /bin/bash
echo "setting up"
sudo apt-get update
sudo apt-get -y install python3 python3-pip
gsutil cp gs://ds561-hw10-wyc/http-client.py /http-client.py