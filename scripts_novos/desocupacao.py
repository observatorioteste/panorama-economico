#!/usr/bin/env python
# coding: utf-8

# BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date 
import util as util
from util import *
from upload import *
trimestre_correto = ['01', '04', '07', '10']

#################################################
#federacoes
lista_unidades_fed = pd.read_html('http://api.sidra.ibge.gov.br/LisUnitTabAPI.aspx?c=4099&n=3&i=P')[1]


#################################################


url = 'http://api.sidra.ibge.gov.br/desctabapi.aspx?c=4099'
data = requests.get(url)
soup = bs(data.content, "html.parser")
periodos = soup.find(id="lblPeriodoDisponibilidade").get_text(strip=True)

lista_periodos = []
periodos = periodos.strip(',').split(', ') 
trimestre_base = 202001

for i in range(len(periodos)):
  trimestre = int(periodos[i])
  if trimestre >= trimestre_base:
    print(trimestre)
    lista_periodos.append(trimestre)


################################## DADOS DO BRASIL ##############################
taxas_brasil = []
for trimestre in lista_periodos:
    # print(mes)
    url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n1/1/p/{0}/f/u'
    url = url.format(trimestre)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    taxa = json.loads(soup.text)
    
    try:

       valor = taxa[1]['V']
       ano = int(str(trimestre)[:4])
       
       if ano >= 2020:
          tri = int(str(trimestre)[4:]) - 1
          tri = str(trimestre_correto[tri])
           
          ano = str(ano)
          trimestr = ano + tri
          print(trimestr)

          trimestre = pd.to_datetime(trimestr, format='%Y%m', errors='coerce')
          trimestre = trimestre.strftime("%Y-%m-%dT%H:%M:%SZ")

          taxas_brasil.append({'x': trimestre, 'y': float(valor)})

    except IndexError:
      break

print('- Série do Brasil foi extraída')

#Ultima taxa nacional
url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n1/1/p/last/f/u'
data = requests.get(url)
soup = bs(data.content, "html5lib")
data_brasil_ultimo = json.loads(soup.text)

trimestres = {'1': 'Jan-Mar/', '2': 'Abr-Jun/', '3': 'Jul-Set/', '4': 'Out-Dez/'}
trimestre_num = data_brasil_ultimo[1]['D3N'][:1]
trimestre_extenso = data_brasil_ultimo[1]['D3N']

referencia_br = trimestres[trimestre_num] + trimestre_extenso[-4:]

indice_brasil_ultimo = data_brasil_ultimo[1]['V']
 
 
tri_atual = taxas_brasil[-2:][1]['y'] 
tri_anterior = taxas_brasil[-2:][0]['y']
indicador_direcao = tri_atual - tri_anterior
if indicador_direcao > 0:
  direcao_br = 'up'
else:
  direcao_br = 'down'


print('- Índice do cartão (Brasil) foi extraído')


################################## GOIAS ##############################

taxas_por_federacao = []
count = 1
trimestre_correto = ['01', '04', '07', '10']
for trimestre in lista_periodos:
  url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n3/52/p/{0}/f/u'
  url = url.format(trimestre)

  data = requests.get(url)
  soup = bs(data.content, "html5lib")
  taxas_json = json.loads(soup.text)
  
  try:

    taxa = taxas_json[1]['V']
    ano = int(str(trimestre)[:4])
    
    if ano >= 2020:
      tri = int(str(trimestre)[4:]) - 1
      tri = str(trimestre_correto[tri])
      # print(tri)
      ano = str(ano)
      trimestr = ano + tri
      # print(trimestr)

      trimestre = pd.to_datetime(trimestr, format='%Y%m', errors='coerce')
      trimestre = trimestre.strftime("%Y-%m-%dT%H:%M:%SZ")

      taxas_por_federacao.append({'x': trimestre, 'y': float(taxa)})

  except IndexError:
    print('Indexação incorreta! Verificar: taxas_json[1][]')
    break

print('- Série de Goiás foi extraída')

taxas_por_federacao = pd.DataFrame(taxas_por_federacao)
taxas_por_federacao = taxas_por_federacao.to_json(orient='records')
taxas_por_federacao = json.loads(taxas_por_federacao)

#ultima taxa de goias
url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n3/52/p/last/f/u'
data = requests.get(url)
soup = bs(data.content, "html5lib")
data_goias = json.loads(soup.text)

trimestres = {'1': 'Jan-Mar/', '2': 'Abr-Jun/', '3': 'Jul-Set/', '4': 'Out-Dez/'}
trimestre_num = data_brasil_ultimo[1]['D3N'][:1]
trimestre_extenso = data_brasil_ultimo[1]['D3N']
referencia_go = trimestres[trimestre_num] + trimestre_extenso[-4:]


indice_goias_ultimo = data_goias[1]['V']

print('- Índice do cartão (Goiás) foi extraído')


tri_atual = taxas_por_federacao[-2:][1]['y'] 
tri_anterior = taxas_por_federacao[-2:][0]['y']
indicador_direcao = tri_atual - tri_anterior
if indicador_direcao > 0:
  direcao_go= 'up'
else:
  direcao_go = 'down'

desocupacao = {
    'nome': 'Taxa de Desocupação',
    'descricao': 'Variação percentual trimestral',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': indice_brasil_ultimo+'%',
            'direcao': direcao_br,
            'desc_serie': 'Variação percentual trimestral',
            'serie_tipo': 'data',
            'referencia': referencia_br,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': taxas_brasil,
        },
        {
            'titulo': 'Goiás',
            'valor': indice_goias_ultimo+'%',
            'direcao': direcao_go,
            'desc_serie': 'Variação percentual trimestral',
            'serie_tipo': 'data',
            'referencia': referencia_go,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': taxas_por_federacao,
        }
    ]
} 


path_save_json = util.config['path_save_json']['path']
name_json = 'desocupacao'
with open(path_save_json+'desocupacao.json', 'w', encoding='utf-8') as f:
    json.dump(desocupacao, f, ensure_ascii=False, indent=4)

print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')
