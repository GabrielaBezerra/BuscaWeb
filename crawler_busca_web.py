#!/usr/bin/env python

# Dependencias
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

# Contadores de busca
passo_busca_profundidade = 0
passo_busca_largura = 0
# Lista de Argumentos
# print(len(sys.argv), "quantidade de argumentos")
# print(len(urlparse(sys.argv[1]).netloc), "url origem")
# print(len(urlparse(sys.argv[2]).netloc), "url destino")

if len(sys.argv) != 3 or len(urlparse(sys.argv[1]).netloc) == 0 or len(urlparse(sys.argv[2]).netloc) == 0:
	print("usage: ./crawler_busca_web <https://www.origem.com> <https://www.destino.com>")
	exit(1)

# URLs iniciais
origem = sys.argv[1]
destino = sys.argv[2]

# Separando as URLs em Componentes
origem_parseada = urlparse(origem)
destino_parseado = urlparse(destino) 

# Separando Palavra Principal do Dominio
titulo_dominio = origem_parseada.netloc.split('.')[1]

# Requisicao GET da origem
resposta = urllib.request.urlopen(origem)
html = resposta.read() # Resposta html em formato String

# Parseando o texto html da resposta em componentes com o BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# BUSCA EM LARGURA
# Encontrando os links dentro da resposta da requsicao
for link in soup.find_all('a'):
	
	# Incrementando passo da busca em largura
	passo_busca_largura = passo_busca_largura + 1

	# Separando o texto do link encontrado em componentes
	url = link.get('href')
	url_parseada = urlparse(url)

	# Organizando os links, e filtrando somente os de dominio diferentes
	if url_parseada.netloc and titulo_dominio not in url_parseada.netloc: 
		print("Dominio diferente encontrado!")
		print(url_parseada.netloc)

		# Incrementando passo da Busca 
		passo_busca_profundidade = passo_busca_profundidade + 1
		
		# TODO: Transformar esse código em função recursiva.

		# BUSCA EM PROFUNDIDADE - Recursiva
		# url_nova_origem = url_parseada.geturl()
		# busca_profundidade_recursiva(url_nova_origem)

		# Problema: loop que faz chamadas recursivas que geram condicoes de parada independentes. 
		# Solucao: Recursao de Recursao (?) ou Flag Global que eh verificada sempre antes do comeco da funcao
