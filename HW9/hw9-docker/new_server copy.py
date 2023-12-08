from __future__ import annotations
from flask import Flask, request
from google.cloud import storage, logging, pubsub_v1
import socket

from google.cloud import compute_v1

project_id = "ds561-wyc-f2023"
region = "us-east1"
instance_name = "hw5--db"

topic_id = "forbidden-access-hw3-ds561"

logging_client = logging.Client(project=project_id)
logname = "HW9-DS561"

logger = logging_client.logger(logname)


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
app = Flask(__name__)


def validate_country(country: str) -> bool:

    return country in ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]

@app.route('/', methods=methods)
def initial():
    return 'Nothing to see here...', 501

@app.route('/<file>', methods=methods)
def getFile(file):
    country = request.headers.get("X-country")
    operation = request.method
    header = request.headers
    gender = header.get("X-gender")
    age = header.get("X-age")
    income = header.get("X-income")
    time_of_day = header.get("X-time")
    client_ip = header.get("X-client-IP")
    if (validate_country(country=country)):
        data_str = "400 Forbidden request detected from {}".format(country)
        data = data_str.encode('utf-8')
        
        future = publisher.publish(topic_path, data)

        logger.log_text(f"PubSub - - - Publisher published to {topic_path} \nResult: {str(future.result())}")
        print(f"PubSub - - - Publisher published to {topic_path} \nResult: {str(future.result())}")

        return "Permission Denied", 400
    elif (operation != "GET"):
        logger.log_text(str(request.method) + file + " requested - - - - - - - 501 Not Implemented")
        print(str(request.method), file, " requested - - - - - - - 501 Not Implemented")

        return 'Not Implemented', 501

    else:
        try:
            storage_client = storage.Client.create_anonymous_client()
            bucket_name = "ds561-bucket"

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file)

            if (blob.exists()):
                content = blob.download_as_text()
                logger.log_text("GET " + file + " - - - - - - - 200 OK")
                print("GET ", file, " - - - - - - - 200 OK")

                return content, 200
            else:
                logger.log_text("GET " + file + " - - - - - - - 404 File Not Found")
                print("GET ", file, " - - - - - - - 404 File Not Found")

                return 'File Not Found', 404
        except:
            logger.log_text(str(request.method) + file + " requested - - - - - - - 501 An Error Occurs while writing database")
            print(str(request.method), file, " requested - - - - - - - 501 An Error Occurs while writing database")

            logger.log_text("Informations of request: {}, {}, {}, {}, {}, {}, {}".format(client_ip, country, gender, age, income, time_of_day, file))

            return 'An Error Occurs while writing database.', 501


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)