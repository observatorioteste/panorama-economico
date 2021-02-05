#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date
import util as util
from util import *
from upload import *


################################## NACIONAL ##############################
# Gera ipca_nacional (JSON)

################### Extração da lista de periodos 
## Formato: 202002 

start = date(2019, 12, 1)
end = date.today()
dates = pd.date_range(start, end, freq='M') + pd.offsets.MonthBegin(n=1)

lista_periodos = []
for i in range(len(dates)):
  year = str(dates[i].year)

  if dates[i].month < 10:
    month = '0' + str(dates[i].month)
    lista_periodos.append(int(year+month))
  else:
    month = str(dates[i].month)
    lista_periodos.append(int(year+month))



#################c# Extração dos dados
#serie
ipca_brasil = []
for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/1737/n1/1/v/63/p/{0}/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    serie_json = json.loads(soup.text)
    
    try:
      valor = serie_json[1]['V']

      mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
      #add indice na serie
      ipca_brasil.append({'x': mes, 'y': valor})

    except IndexError:
      break
    
print('- Dados do Brasil foram extraídos')
print('- Série (Brasil) criada')
################### Referencia  
#formato 202011
referencia = ipca_brasil[-1:][0]['x']
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

#formato Jan/2020
referencia = str(referencia)[:7]
mes_cod = int(referencia[5:] )
mes_nome = meses_ano[mes_cod-1]
ano = str(referencia[:4])
referencia_br = mes_nome + '/' + ano
referencia_br

####################cartao nacional
url = 'http://api.sidra.ibge.gov.br/values/t/1737/n1/1/p/{0}/v/63/f/u'
url = url.format(referencia.replace("-", ''))
data = requests.get(url)
soup = bs(data.content, "html5lib")
valor_cartao_br = json.loads(soup.text)

try:
  valor_cartao_br = valor_cartao_br[1]['V']

except IndexError:
   valor = '#'   

valor_cartao_br = float(valor_cartao_br)
if valor_cartao_br < 0:
  direcao_br = "down"
  valor_cartao_br = valor_cartao_br[1:]
else:
  direcao_br = 'up'

print('- Valor do cartão (Brasil) armazenado')

################################## REGIONAL ##############################
# Gera ipca_regional (JSON)

################### Extração da lista de periodos 
## Formato: 202002 

start = date(2019, 12, 1)
end = date.today()
dates = pd.date_range(start, end, freq='M') + pd.offsets.MonthBegin(n=1)

lista_periodos = []
for i in range(len(dates)):
  year = str(dates[i].year)

  if dates[i].month < 10:
    month = '0' + str(dates[i].month)
    lista_periodos.append(int(year+month))
  else:
    month = str(dates[i].month)
    lista_periodos.append(int(year+month))


ipca_goias = []
################### Extração da variacao mensal
for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/7060/n6/5208707/p/{0}/v/63/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    serie_json = json.loads(soup.text)
    
    try:
      valor = serie_json[1]['V']

      mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

      #add indice na serie
      ipca_goias.append({'x': mes, 'y': valor})

    except IndexError:
      break

print('- Dados de Goiás foram extraídos')
print('- Série (Goiás) criada')
################### Extração da variacao acumulada ano

################### Referencia  
#formato 202011
referencia = ipca_goias[-1:][0]['x']

#formato Jan/2020
referencia = str(referencia)[:7]
mes_cod = int(referencia[5:] )
mes_nome = meses_ano[mes_cod-1]
ano = str(referencia[:4])
referencia_go = mes_nome + '/' + ano
referencia_go

########### Extração
url = 'http://api.sidra.ibge.gov.br/values/t/7060/n6/5208707/p/{0}/v/63/f/u'
url = url.format(referencia.replace("-", ''))
data = requests.get(url)
soup = bs(data.content, "html5lib")
valor_cartao_go = json.loads(soup.text)

try:
  valor_cartao_go = valor_cartao_go[1]['V']

except IndexError:
   valor = '#'   

valor_cartao_go = float(valor_cartao_go)

if valor_cartao_go < 0:
  direcao_go = "down"
  valor_cartao_go = valor_cartao_go[1:]
else:
  direcao_go = 'up'

print('- Valor do cartão (Goiás) foi armazenado')
ipca_json = {
    'nome': 'Índice Nacional de Preços ao Consumidor Amplo - IPCA',
    'descricao': 'Variação percentual mensal',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(valor_cartao_br) +'%',
            'direcao': direcao_br,
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': referencia_br,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': ipca_brasil,
        },
        {
            'titulo': 'Goiás',
            'valor': str(valor_cartao_go)+'%',
            'direcao': direcao_go,
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': referencia_go,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': ipca_goias,
        }
    ]
}


path_save_json = util.config['path_save_json']['path']
name_json = 'ipca'

################### Salva o ipca_mesclagem.JSON 
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(ipca_json, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')