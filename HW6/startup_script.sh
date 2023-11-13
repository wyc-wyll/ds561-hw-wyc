#! /bin/bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
python3 -m pip install pymysql
python3 -m pip install sqlalchemy
python3 -m pip install "cloud-sql-python-connector[pymysql]"

python3 -m pip install scikit-learn
python3 -m pip install numpy


# sudo apt-get install -y wget

# export DEB_FILE=mysql-apt-config_0.8.20-1_all.deb
# cd /tmp
# curl -L --output ${DEB_FILE} \
#     https://dev.mysql.com/get/${DEB_FILE}

# cat > ${DEB_FILE}.md5 << EOL
# 799bb0aefb93d30564fa47fc5d089aeb ${DEB_FILE}
# EOL
# md5sum --check ${DEB_FILE}.md5

# sudo dpkg -i ${DEB_FILE}

# sudo apt-key adv \
#     --keyserver keyserver.ubuntu.com \
#     --recv-keys 467B942D3A79BD29

# sudo apt-get update

# sudo apt-get -y install mysql-community-server