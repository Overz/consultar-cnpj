from lxml.html import fromstring, tostring, re, soupparser
from flask import Flask, json, request
from waitress import serve
from requests import get


API = Flask(__name__)
CNPJ_ROCSK = 'https://cnpjs.rocks/cnpj/'
RECEITA_WS = 'http://receitaws.com.br/v1/cnpj/'
PORT = 3000
MANY_REQUESTS_STATUS = 429

# formatador: autopep8 -i handler.py
@API.route('/', methods=['POST'])
def main():
    try:
        CNPJ = request.json['cnpj']

        page_receita = get(RECEITA_WS + CNPJ)
        body_receita = tostring(fromstring(page_receita.content))
        receita_result = soupparser.BeautifulSoup(
            body_receita, 'html.parser').text
        receita_json = receita_result.replace('<p>', '').replace('</p>', '')

        if page_receita.status_code != MANY_REQUESTS_STATUS:
            return json.loads(receita_json), 200
        else:
            page_rocks = get(CNPJ_ROCSK + CNPJ)
            body_rocks = tostring(fromstring(page_rocks.content))
            rocks_result = soupparser.BeautifulSoup(
                body_rocks, 'html.parser').find_all('li')
            rocks_json = replace(str(rocks_result))

            return json.loads(rocks_json), 200
    except Exception as ex:
        print('\nVariavel recebida não é acessível!')
        print('Err:', ex, '\n')
        return json.dumps({'error': 'Internal Server Error'}), 500


@API.route('/healthcheck', methods=['GET'])
def check():
    return json.dumps({"ok": True})


def replace(li: str):
    tagA = re.compile(r'(<li><a.+>(.+)</a></li>)')
    filtered = re.sub(tagA, '', li)
    replaced = filtered.replace('<li>', '"').replace(
        '</strong></li>', '"').replace(':', '":').replace('<strong>', '"').replace('[', '{')
    last_char = replaced.rfind(',')
    return replaced[:last_char] + "}"


if __name__ == "__main__":
    serve(API, port=PORT)
