FROM python:alpine

ENV SITE_URL="https://cnpjs.rocks/cnpj/"
ENV PORT=3000

WORKDIR /app
COPY ./src .
COPY requirements.txt .

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "handler.py" ]