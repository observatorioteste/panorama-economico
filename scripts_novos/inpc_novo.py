from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date
import util as util
from util import *
from upload import *

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

def cath_referencia(mes):
  if mes[:3] == 'jan':
      mes = 'Jan/'+(str(mes[-4:])).capitalize()
  else:
      mes = 'Jan-'+(mes[:3]+ '/' +mes[-4:]).capitalize()

  return mes

def define_direcao(valor):
  if float(valor) < 0:
    return {'direcao': 'down', 'valor': str(valor)[1:]}

  else:
    return {'direcao': 'up', 'valor': valor}

def cath_cartao():
  
  for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/7063/n1/1/p/{0}/v/44/N6/5208707/f/u'
    url = url.format(mes)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)

    try:
      valor = dados[1]['V']
      if str(valor) != '...':
        mes_referencia = dados[1]['D2N']
        ultimo_dado_br= {'mes': mes_referencia, 'valor': valor}
      
      valor = dados[2]['V']      
      if str(valor) != '...':
        mes_referencia = dados[2]['D2N']
        ultimo_dado_go= {'mes': mes_referencia, 'valor': valor}
    
    except IndexError:
      break

  ultimo_dado_go.update({
      'referencia_traduzida': cath_referencia(ultimo_dado_go['mes']), 
      'direcao': define_direcao(ultimo_dado_go['valor'])['direcao'],
      'valor': define_direcao(ultimo_dado_go['valor'])['valor']
  })

  ultimo_dado_br.update({
      'referencia_traduzida': cath_referencia(ultimo_dado_br['mes']), 
      'direcao': define_direcao(ultimo_dado_br['valor'])['direcao'],
      'valor': define_direcao(ultimo_dado_br['valor'])['valor']
  })

  return {'cartao_br': ultimo_dado_br, 'cartao_go': ultimo_dado_go}  


def cath_serie():
  serie_go = []
  serie_br = []
  for mes in lista_periodos:
    
    url = 'http://api.sidra.ibge.gov.br/values/t/7063/n1/1/p/{0}/v/44/N6/5208707/f/u'
    url = url.format(mes)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)
    try:
      mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

      valor_go = dados[1]['V']
      mes_referencia = dados[1]['D2N']
      if str(valor_go) != '...':
        serie_go.append({'x': mes, 'y': float(valor_go)})

      valor_br = dados[2]['V']
      mes_referencia = dados[2]['D2N']
      if str(valor_br) != '...':
        serie_br.append({'x': mes, 'y': float(valor_br)})
    
    except IndexError:
      break

  return {'serie_go': serie_go, 'serie_br': serie_br}      
 
cartoes = cath_cartao()
series = cath_serie()

ipca_json = {
    'nome': 'Índice Nacional de Preços ao Consumidor Amplo - IPCA',
    'descricao': 'Variação percentual mensal',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': cartoes['cartao_br']['valor']+'%',
            'direcao': cartoes['cartao_br']['direcao'],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartoes['cartao_br']['referencia_traduzida'],
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': series['serie_br'],
        },
        {
            'titulo': 'Goiás',
            'valor': cartoes['cartao_go']['valor']+'%',
            'direcao':  cartoes['cartao_go']['direcao'],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartoes['cartao_go']['referencia_traduzida'],
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': series['serie_go'],
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