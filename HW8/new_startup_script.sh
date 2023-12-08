#! /bin/bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
python3 -m pip install flask
python3 -m pip install google-cloud-storage
python3 -m pip install google-cloud-pubsub
python3 -m pip install google-cloud-logging
python3 -m pip install flask_cors
python3 -m pip install functions-framework
python3 -m pip install pymysql
python3 -m pip install sqlalchemy
python3 -m pip install google-cloud-compute
python3 -m pip install "cloud-sql-python-connector[pymysql]"

gsutil cp gs://ds561-bucket/app1.py /app1.py