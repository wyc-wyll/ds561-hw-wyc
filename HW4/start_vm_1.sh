#! /bin/bash

echo "setting up"

sudo apt-get update
sudo apt-get -y install python3 python3-pip
python3 -m pip install flask
python3 -m pip install google-cloud-storage
python3 -m pip install google-cloud-pubsub
python3 -m pip install google-cloud-logging
python3 -m pip install flask_cors
python3 -m pip install functions-framework

gsutil cp gs://hw2-ds561/app1.py /app1.py

python3 ./app1.py