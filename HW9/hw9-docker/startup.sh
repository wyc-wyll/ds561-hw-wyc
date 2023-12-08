#! /bin/bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
python3 -m pip install flask
python3 -m pip install google-cloud-storage
python3 -m pip install google-cloud-pubsub
python3 -m pip install google-cloud-logging
python3 -m pip install flask_cors
python3 -m pip install beautifulsoup4
# python3 -m pip install pymysql
# python3 -m pip install sqlalchemy
python3 -m pip install google-cloud-compute
# python3 -m pip install "cloud-sql-python-connector[pymysql]"

python3 ./new_server.py