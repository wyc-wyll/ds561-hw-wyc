FROM python:3.9.18-slim-bullseye

COPY ./requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

COPY ./new_server.py /

EXPOSE 8080

ENTRYPOINT [ "python3" ]

CMD [ "/new_server.py" ]