#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import urllib.parse
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from util import *
from upload import *
from datetime import datetime
import ssl #https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho


################################## PAGINA GOIAS ##############################
url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/5'
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html5lib')

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
estados = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json
goias = estados['data'][8]['url']

url = goias
response = requests.get(url, verify=False)

soup = BeautifulSoup(response.content, 'html5lib')

importacoes_porcentagem_go = soup.find_all(class_="count_bottom")[1].text.strip().split("%")[0]
importacoes_referencia_go = soup.find_all(class_="count_bottom")[1].text.strip()[-19:]
exportacoes_porcentagem_go = soup.find_all(class_="count_bottom")[0].text.strip().split("%")[0]
exportacoes_referencia_go = soup.find_all(class_="count_bottom")[0].text.strip()[-19:]

print('- Dados de Goiás extraídos')
################### referencia
exportacoes_referencia_go = (exportacoes_referencia_go.replace("  ", " ").replace(exportacoes_referencia_go[-5:], '').replace(exportacoes_referencia_go[9:-5], "/"+exportacoes_referencia_go[10:-5]))[1:]
importacoes_referencia_go = (importacoes_referencia_go.replace("  ", " ").replace(importacoes_referencia_go[-5:], '').replace(importacoes_referencia_go[9:-5], "/"+importacoes_referencia_go[10:-5]))[1:]


#################### Direcao seta
importacoes_porcentagem_go = importacoes_porcentagem_go.replace(',', '.')
if float(importacoes_porcentagem_go) < 0:
  direcao_imp_go = 'down'
  importacoes_porcentagem_go = importacoes_porcentagem_go[1:]
else:
  direcao_imp_go = 'up'

exportacoes_porcentagem_go = exportacoes_porcentagem_go.replace(',', '.')
if float(exportacoes_porcentagem_go) < 0:
  direcao_exp_go = 'down'
  exportacoes_porcentagem_go = exportacoes_porcentagem_go[1:]
else:
  direcao_exp_go = 'up'


##################################  SERIE GOAIS ##############################

html = urllib.request.urlopen(goias)
goias_data = BeautifulSoup(html, 'lxml')
goias_data = goias_data.select('#goiás-série-histórica')
goias_data = goias_data[0].find('script', type='application/json') 


now = datetime.now()
ano_atual = now.year
ano_anterior = ano_atual - 1

json_goias = json.loads(goias_data.contents[0])
 
data_go_exp = []
data_go_imp = []

for item in range(len(json_goias['x']['data'])):
  ano = int(json_goias['x']['data'][item]['CO_ANO'])
  tipo = json_goias['x']['data'][item]["TIPO"]
  if (ano == ano_anterior or ano == ano_atual) and tipo == "EXP":
    data_go_exp.append(json_goias['x']['data'][item])

  if (ano == ano_anterior or ano == ano_atual) and tipo == "IMP":
    data_go_imp.append(json_goias['x']['data'][item])

serie_go_imp = []
serie_go_exp = []

for row in data_go_imp:
  if(row['PERIODO'] == 'Total'):
    mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

    fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
    fob = fob +',00'


    serie_go_imp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})
 
for row in data_go_exp:
  if(row['PERIODO'] == 'Total'):
    mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

    fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
    fob = fob +',00'

    serie_go_exp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})
 
print('- Série com dados de Goiás criada')

##################################  CARDS BRASIL ##############################
url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/1'
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html5lib')

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
brasil = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json
url = brasil['data'][0]['url']

response = requests.get(url, verify=False)

soup = BeautifulSoup(response.content, 'html5lib')

importacoes_porcentagem_br = soup.find_all(class_="count_bottom")[1].text.strip().split("%")[0]
importacoes_referencia_br = soup.find_all(class_="count_bottom")[1].text.strip()[-19:]
exportacoes_porcentagem_br = soup.find_all(class_="count_bottom")[0].text.strip().split("%")[0]
exportacoes_referencia_br = soup.find_all(class_="count_bottom")[0].text.strip()[-19:]

print('- Dados do Brasil extraídos')
################### referencia
exportacoes_referencia_br = (exportacoes_referencia_br.replace("  ", " ").replace(exportacoes_referencia_br[-5:], '').replace(exportacoes_referencia_br[9:-5], "/"+exportacoes_referencia_br[10:-5]))[1:]
importacoes_referencia_br = (importacoes_referencia_br.replace("  ", " ").replace(importacoes_referencia_br[-5:], '').replace(importacoes_referencia_br[9:-5], "/"+importacoes_referencia_br[10:-5]))[1:]


#################### Direcao seta
importacoes_porcentagem_br = importacoes_porcentagem_br.replace(',', '.')
if float(importacoes_porcentagem_br) < 0:
  direcao_imp_br = 'down'
  importacoes_porcentagem_br = importacoes_porcentagem_br[1:]
else:
  direcao_imp_br = 'up'

exportacoes_porcentagem_br = exportacoes_porcentagem_br.replace(',', '.')
if float(exportacoes_porcentagem_br) < 0:
  direcao_exp_br = 'down'
  exportacoes_porcentagem_br = exportacoes_porcentagem_br[1:]
else:
  direcao_exp_br = 'up'

##################################  SERIE BRASIL ##############################

url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/1'

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
brasil_url = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json

brasil_url = brasil_url['data'][0]['url']
brasil_page = urlopen(brasil_url)
brasil_page = BeautifulSoup(brasil_page, 'lxml')
brasil_page = brasil_page.select('#série-histórica')
data_brasil = brasil_page[0].find('script', type='application/json') 
 
now = datetime.now()
ano_atual = now.year
ano_anterior = ano_atual - 1

json_brasil = json.loads(data_brasil.contents[0])
 
data_br_exp = []
data_br_imp = []

for item in range(len(json_brasil['x']['data'])):
  ano = int(json_brasil['x']['data'][item]['CO_ANO'])
  tipo = json_brasil['x']['data'][item]["TIPO"]
  if (ano == ano_anterior or ano == ano_atual) and tipo == "EXP":
    data_br_exp.append(json_brasil['x']['data'][item])

  if (ano == ano_anterior or ano == ano_atual) and tipo == "IMP":
    data_br_imp.append(json_brasil['x']['data'][item])

serie_br_imp = []
serie_br_exp= []

for row in data_br_imp:
  if(row['PERIODO'] == 'Total'):
    mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

    fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
    fob = 'US$ ' + fob +',00'

    print(row['var_per'][:-1])
    serie_br_imp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})

for row in data_br_exp:
  if(row['PERIODO'] == 'Total'):
    mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

    fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
    fob = 'US$ ' +fob +',00'

    serie_br_exp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})

print('- Série com dados de Goiás criada')

comex_importacao = {
    'nome': 'Importações',
    'descricao': 'Variação percentual em relação ao mesmo período do ano anterior',
    'fonte': 'MDIC',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(importacoes_porcentagem_br) +'%',
            'direcao': direcao_imp_br,
            'desc_serie': 'Variação percentual e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia':importacoes_referencia_br,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'y2_label': {
                'prefixo_sufixo': 'prefixo',
                'label': 'US$'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação',
                'y2': 'Valor'
            },
            'serie': serie_br_imp,
        },
        {
            'titulo': 'Goiás',
            'valor': str(importacoes_porcentagem_go) +'%',
            'direcao': direcao_imp_go,
            'desc_serie': 'Variação percentual e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': importacoes_referencia_go,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'y2_label': {
                'prefixo_sufixo': 'prefixo',
                'label': 'US$'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação',
                'y2': 'Valor'
            },
            'serie': serie_go_imp,
        },
    ]
}

path_save_json = util.config['path_save_json']['path']
name_json = 'comex_importacao'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(comex_importacao, f, ensure_ascii=False, indent=4)
# print('- JSON Importações armazenado')

######################
#Upload
upload_files_to_github(name_json)


# #################################################
#EXPORTACAO

comex_exportacao = {
    'nome': 'Exportações',
    'descricao': 'Variação percentual em relação ao mesmo período do ano anterior',
    'fonte': 'MDIC',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(exportacoes_porcentagem_br) +'%' ,
            'direcao': direcao_exp_br,
            'desc_serie': 'Variação percentual e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia':exportacoes_referencia_br,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'y2_label': {
                'prefixo_sufixo': 'prefixo',
                'label': 'US$'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação',
                'y2': 'Valor FOB'
            },
            'serie': serie_br_exp,
        },
        {
            'titulo': 'Goiás',
            'valor': str(exportacoes_porcentagem_go) +'%',
            'direcao': direcao_exp_go,
            'desc_serie': 'Variação percentual e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': exportacoes_referencia_go,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'y2_label': {
                'prefixo_sufixo': 'prefixo',
                'label': 'US$'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação',
                'y2': 'Valor FOB'
            },
            'serie': serie_go_exp,
        },
    ]
}

path_save_json = util.config['path_save_json']['path']
name_json = 'comex_exportacao'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(comex_exportacao, f, ensure_ascii=False, indent=4)

######################
#Upload
upload_files_to_github(name_json)
print('- JSONs enviados para o GitHub')
