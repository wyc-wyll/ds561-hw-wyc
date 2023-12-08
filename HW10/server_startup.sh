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
python3 -m pip install pymysql
python3 -m pip install sqlalchemy
python3 -m pip install "cloud-sql-python-connector[pymysql]"
gsutil cp gs://ds561-hw10-wyc/server.py /server.py
gsutil cp gs://ds561-hw10-wyc/generate-content.py /generate.py
python3 ./generate.py
gsutil cp ./*.html gs://ds561-hw10-wyc/
python3 ./server.py