from flask import Flask, request
from google.cloud import storage, logging, pubsub_v1
from google.cloud.sql.connector import Connector
import sqlalchemy

connector = Connector()

project_id = "ds561-wyc-f2023"
region = "us-east1"
instance_name = "hw5--db"

# initialize parameters
INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = "454604"
DB_NAME = "hw5"


def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

topic_id = "forbidden-access-hw3-ds561"

logging_client = logging.Client(project=project_id)
logname = "HW4-DS561"

logger = logging_client.logger(logname)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
app = Flask(__name__)

insert_request = sqlalchemy.text(
    "INSERT INTO Request (client_ip, country, gender, age, income, time_of_day, requested_file) VALUES (:client_ip, :country, :gender, :age, :income, :time_of_day, :requested_file);",
)

insert_country = sqlalchemy.text(
    "INSERT INTO Ban_status (country) VALUES (:country);",
)

insert_error = sqlalchemy.text(
    "INSERT INTO Error_log (time_of_day, requested_file, error_code) VALUES (:time_of_day, :requested_file, :error_code);"
)

def validate_country(country: str) -> bool:

    return country in ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]

def insertRequestTable(client_ip: str, country: str, gender: str, age: str, income: str, time_of_day: str, requested_file: str):
    with pool.connect() as db_conn:
        print("updating request list")
        db_conn.execute(insert_request, parameters={"client_ip": client_ip, "country": country, "gender": gender, "age": age, "income": income, "time_of_day": time_of_day, "requested_file": requested_file})

        db_conn.commit()

def insertError_logTable(time_of_day: str, requested_file: str, error_code: int):
    with pool.connect() as db_conn:
        print("updating error list")
        db_conn.execute(insert_error, parameters={"time_of_day": time_of_day, "requested_file": requested_file, "error_code": error_code})

        db_conn.commit()

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

        insertError_logTable(time_of_day=time_of_day, requested_file=file, error_code=400)

        return "Permission Denied", 400
    elif (operation != "GET"):
        logger.log_text(str(request.method) + file + " requested - - - - - - - 501 Not Implemented")
        print(str(request.method), file, " requested - - - - - - - 501 Not Implemented")

        insertError_logTable(time_of_day=time_of_day, requested_file=file, error_code=501)
            
        return 'Not Implemented', 501
    
    else:
        try:
            storage_client = storage.Client.create_anonymous_client()
            bucket_name = "hw2-ds561"

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file)

            if (blob.exists()):
                content = blob.download_as_text()
                logger.log_text("GET " + file + " - - - - - - - 200 OK")
                print("GET ", file, " - - - - - - - 200 OK")

                insertRequestTable(client_ip=client_ip, country=country, 
                                   gender=gender, age=age, 
                                   income=income, time_of_day=time_of_day, 
                                   requested_file=file)
                
                return content, 200
            else:
                logger.log_text("GET " + file + " - - - - - - - 404 File Not Found")
                print("GET ", file, " - - - - - - - 404 File Not Found")

                insertError_logTable(time_of_day=time_of_day, requested_file=file, error_code=404)

                return 'File Not Found', 404
        except:
            logger.log_text(str(request.method) + file + " requested - - - - - - - 501 An Error Occurs while writing database")
            print(str(request.method), file, " requested - - - - - - - 501 An Error Occurs while writing database")

            logger.log_text("Informations of request: {}, {}, {}, {}, {}, {}, {}".format(client_ip, country, gender, age, income, time_of_day, file))

            insertError_logTable(time_of_day=time_of_day, requested_file=file, error_code=501)
            
            return 'An Error Occurs while writing database.', 501
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    connector.close()