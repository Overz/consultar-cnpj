from lxml.html import fromstring as parser, tostring, re, soupparser as bs4
from flask import Flask, json, request as req
from waitress import serve
from requests import get

CNPJ_ROCSK = 'https://cnpjs.rocks/cnpj/'
RECEITA_WS = 'http://receitaws.com.br/v1/cnpj/'
PORT = 3000
MANY_REQUESTS_STATUS = 429
PAGE_CODE = 0

def handle():
    try:
        CNPJ = req.json['cnpj']
        receita_json = receita_ws(CNPJ)

        if PAGE_CODE != MANY_REQUESTS_STATUS:
            return json.loads(receita_json), 200
        else:
            return json.loads(cnpj_rocks(CNPJ)), 200
    except Exception as ex:
        print('\nVariavel recebida não é acessível! Var:', CNPJ)
        print('Err:', ex, '\n')
        return json.dumps({'error': 'Internal Server Error', 'cnpj': CNPJ}), 500


def receita_ws(cnpj: str) -> str:
    global PAGE_CODE
    
    page_receita = get(RECEITA_WS + cnpj)
    PAGE_CODE = page_receita.status_code

    body_receita = tostring(parser(page_receita.content))
    
    receita_result = bs4.BeautifulSoup(
        body_receita, 'html.parser').text
    
    return receita_result[:1] + '"from": "RECEITA_WS",' + \
        receita_result[1:].replace('<p>', '').replace('</p>', '')


def cnpj_rocks(cnpj: str) -> str:
    page_rocks = get(CNPJ_ROCSK + cnpj)
    body_rocks = tostring(parser(page_rocks.content))
    rocks_result = bs4.BeautifulSoup(
        body_rocks, 'html.parser').find_all('li')
    
    return replace(str(rocks_result))


def replace(li: str) -> str:
    tagA = re.compile(r'(<li><a.+>(.+)</a></li>)')
    filtered = re.sub(tagA, '', li)
    replaced = filtered.replace('<li>', '"').replace(
        '</strong></li>', '"').replace(':', '":').replace('<strong>', '"').replace('[', '{ "from": "CNPJ_ROCKS", ')
    last_char = replaced.rfind(',')
    return replaced[:last_char] + "}"