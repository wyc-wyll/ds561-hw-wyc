#! /bin/bash
echo "setting up"
sudo apt-get update
sudo apt-get -y install python3 python3-pip
python3 -m pip install google-cloud-pubsub
gsutil cp gs://ds561-hw10-wyc/listener.py /listener.py