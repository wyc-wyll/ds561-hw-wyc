from google.cloud import storage
import flask
import functions_framework
from google.cloud import logging
from google.cloud import pubsub_v1
import requests

project_id = "ds561-wyc-5304"
topic_id = "forbidden-access-hw3-ds561"

def validate_country(country: str) -> bool:
    return country in ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]

@functions_framework.http
def getFile(request: flask.Request):
    path = request.path
    filename = path.split("/")[-1]

    project_id = "ds561-wyc-5304"
    logging_client = logging.Client(project=project_id)
    logname = "HW3-DS561"

    logger = logging_client.logger(logname)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)


    data_str = "Machine Started"
    data = data_str.encode('utf-8')
    future = publisher.publish(topic_path, data)

    # ip = request.headers["X-Forward-For"]
    # payload = {'key': '8D92129DF050115AF4E3AAE652584062', 'ip': str(ip)}
    # location_result = requests.get("https://api.ip2location.io/", params=payload)
    # country = location_result.json().get("country_name")

    country = request.headers["X-country"]

    if (validate_country(country=country)):

        data_str = "400 Forbidden request detected from {}".format(country)
        data = data_str.encode('utf-8')
        future = publisher.publish(topic_path, data)

        logger.log_text(f"PubSub - - - Publisher published to {topic_path} \nResult: {str(future.result())}")
        print(f"PubSub - - - Publisher published to {topic_path} \nResult: {str(future.result())}")

        return "Permission Denied", 400

    try:
        if (request.method == 'GET'):
            
            storage_client = storage.Client.create_anonymous_client()
            bucket_name = "hw2-ds561"

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)

            if (blob.exists()):
                content = blob.download_as_text()
                logger.log_text("GET " + filename + " - - - - - - - 200 OK")
                print("GET ", filename, " - - - - - - - 200 OK")
                return content, 200
            else:
                logger.log_text("GET " + filename + " - - - - - - - 404 File Not Found")
                print("GET ", filename, " - - - - - - - 404 File Not Found")
                return 'File Not Found', 404

        else:
            logger.log_text(str(request.method) + filename + " requested - - - - - - - 501 Not Implemented")
            print(str(request.method), filename, " requested - - - - - - - 501 Not Implemented")
            return 'Not Implemented', 501
    except:
        logger.log_text("No Method Used - - - Undefined")
        print("No Method Used - - - Undefined")
        return "Nothing Requested", 501
        