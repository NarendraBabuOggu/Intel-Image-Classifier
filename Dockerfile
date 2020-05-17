FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc


COPY requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
