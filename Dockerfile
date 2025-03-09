FROM python:3.13-alpine

WORKDIR /app
RUN mkdir /app/data
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY tasklist tasklist

CMD [ "fastapi", "run", "./tasklist/main.py"]
