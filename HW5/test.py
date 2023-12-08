from flask import Flask, request

app = Flask(__name__)

methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]


@app.route('/', methods=methods)
def initial():
    return 'Nothing to see here...', 501

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)