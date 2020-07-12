#!/usr/bin/env python

# Dependencias
import sys
import json
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

banner = """
 ____                    __        __   _     
| __ ) _   _ ___  ___ __ \ \      / /__| |__  
|  _ \| | | / __|/ __/ _` \ \ /\ / / _ \ '_ \ 
| |_) | |_| \__ \ (_| (_| |\ V  V /  __/ |_) |
|____/ \__,_|___/\___\__,_| \_/\_/ \___|_.__/ 

Many pages make a thick book.
"""
print(banner)

# Script Info
scriptname = "crawler_busca_web"
param1 = "<https://www.origem.com>"
param2 = "<https://www.destino.com>"
usage = "usage: ./"+scriptname+" "+param1+" "+param2+"\n"


# Input verification
verify_params_quant = len(sys.argv) != 3
if verify_params_quant:
    exit(usage)

param1_verify = len(urlparse(sys.argv[1]).netloc) == 0
param2_verify = len(urlparse(sys.argv[2]).netloc) == 0
if param1_verify or param2_verify:
    exit(usage)


# VARIABLES AND CONSTANTS

# Limite de busca
limite = 3

# Contadores de busca
passo_busca_profundidade = 0
passo_busca_largura = 0

# URLs iniciais
origem = sys.argv[1]
destino = sys.argv[2]

# Separando as URLs em Componentes
origem_parsed = urlparse(origem)
destino_parsed = urlparse(destino)

# Seen URLs
seen_urls = {}


# FUNCTIONS
def get_domain(url):
    return url.removing


def search_destiny(last_urls, current_url_parsed):
    global destino_parsed, passo_busca_profundidade, passo_busca_largura

    print("Checking", current_url_parsed)

    last_urls.append(current_url_parsed)

    urls_to_check = []

    # Incrementando passo da Busca em Profundidade:
    #   Cada requisicao esta sendo contada como um passo de
    #   busca em profundidade.
    passo_busca_profundidade = passo_busca_profundidade + 1
    seen_urls[current_url_parsed] = []

    # Requisicao GET da origem
    resposta = urllib.request.urlopen(origem)
    html = resposta.read()  # Resposta html em formato String

    # Parseando o texto html da resposta em componentes
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrando os links dentro da resposta da requsicao
    for link in soup.find_all('a'):

        # Incrementando passo da Busca em Largura.
        #   Cada link encontrado em cada pagina esta sendo contado como
        #   um passo de busca em largura, mesmo que jã tenha sido visto.
        passo_busca_largura = passo_busca_largura + 1

        # Separando o texto do link encontrado em componentes
        url = link.get('href')
        url_parsed = urlparse(url).netloc

        # Organizando os links
        # Filtrando somente os de dominio diferentes
        not_request_domain = current_url_parsed not in url_parsed
        # print(current_url_parsed,url_parsed)

        has_not_be_seen = True
        for key, value in seen_urls.items():
            if url_parsed in value or url_parsed == key:
                has_not_be_seen = False

        if url_parsed and not_request_domain and has_not_be_seen:

            seen_urls[current_url_parsed].append(url_parsed)

            print("Dominio diferente encontrado! "+url_parsed)
            print("Destiny:                      "+destino_parsed.netloc)
            print("\n")

            if url_parsed in destino_parsed.netloc:
                end = {
                    'found': True,
                    'passo_busca_largura': passo_busca_largura,
                    'passo_busca_profundidade': passo_busca_profundidade,
                    'checked_urls_amount': len(seen_urls.keys()),
                    'path': last_urls,
                    'seen_urls': seen_urls,
                }
                result_log = json.dumps(end, indent=4)
                exit(result_log)
            else:
                urls_to_check.append(url_parsed)
                # search_destiny(last_urls, url)

    print(urls_to_check)
    for new_url in urls_to_check:
        search_destiny(last_urls, new_url)

# MAIN

search_destiny([], origem_parsed.netloc)


# TODO: Transformar esse código em função recursiva.

# BUSCA EM PROFUNDIDADE - Recursiva
# url_nova_origem = url_parseada.geturl()
# busca_profundidade_recursiva(url_nova_origem)

# Problema:
# loop que faz chamadas recursivas que geram condicoes de
# parada independentes.

# Solucao:
# Recursao de Recursao (?) ou Flag Global que eh verificada
# sempre antes do comeco da funcao
