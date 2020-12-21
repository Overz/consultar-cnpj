FROM python:alpine

WORKDIR /app
COPY ./src .
COPY requirements.txt .

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "index.py"]
