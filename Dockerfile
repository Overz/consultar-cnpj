FROM python:alpine

# docker run -p 3000:3000 -it py/teste ash

RUN apk --update --no-cache add curl

HEALTHCHECK --interval=5s --timeout=30s --start-period=2m CMD [ "curl", "localhost:3000/healthcheck" ] || exit 1

WORKDIR /app
COPY ./src .
COPY requirements.txt .

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "handler.py" ]