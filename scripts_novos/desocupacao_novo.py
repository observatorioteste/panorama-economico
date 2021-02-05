from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date 
import util as util
from util import *
from upload import *

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

def cath_trimestre(trimestre_dados):

  trimestres_ano = ['01', '04', '07', '10']

  ano = int(str(trimestre_dados)[-4:])
  trimestre_num = int(str(trimestre_dados)[:1]) - 1
  trimestre_num = str(trimestres_ano[trimestre_num])

  ano = str(ano)
  trimestre_modificado = ano + trimestre_num

  trimestre_modificado = pd.to_datetime(trimestre_modificado, format='%Y%m', errors='coerce')
  trimestre_modificado = trimestre_modificado.strftime("%Y-%m-%dT%H:%M:%SZ")

  return trimestre_modificado

def cath_serie():
  serie_go = []
  serie_br = []
  for trimestre in lista_periodos:
    
    url = 'http://api.sidra.ibge.gov.br/values/t/4099/n1/1/p/{0}/v/4099/N3/52/f/u'
    url = url.format(trimestre)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)
    try:

      valor_go = dados[1]['V']      
      
      if str(valor_go) != '...':
        ultimo_trimestre_go = dados[1]['D2N'][:1]
        trimestre_referencia = dados[1]['D2N']
        trimestre_referencia = cath_trimestre(trimestre_referencia)
                
        serie_go.append({'x': trimestre_referencia, 'y': float(valor_go)})

      valor_br = dados[2]['V']
      
      if str(valor_br) != '...':
        ultimo_trimestre_br = dados[1]['D2N'][:1]
        trimestre_referencia = dados[2]['D2N']
        trimestre_referencia = cath_trimestre(trimestre_referencia)
        serie_br.append({'x': trimestre_referencia, 'y': float(valor_br)})
    
    except IndexError:
      break

  return {'serie_go': serie_go, 'serie_br': serie_br, 'ultimo_trimestre_br': ultimo_trimestre_br, 'ultimo_trimestre_go': ultimo_trimestre_go}     

def cath_cartoes(series):
  trimestre_para_cartao = {'1': 'Jan-Mar/', '2': 'Abr-Jun/', '3': 'Jul-Set/', '4': 'Out-Dez/'}
  valor_cartao_br = str(series['serie_br'][-1:][0]['y'])
  valor_cartao_go = str(series['serie_go'][-1:][0]['y'])
  ultimo_trimestre_go = trimestre_para_cartao[series['ultimo_trimestre_go']]
  ultimo_trimestre_br = trimestre_para_cartao[series['ultimo_trimestre_br']]

  if float(valor_cartao_br) > 0:
    direcao_br = 'up'
  else:
    direcao_br = 'down'
    valor_cartao_br = str(valor_cartao_br)[1:]

  if float(valor_cartao_go) > 0:
    direcao_go = 'up'
  else:
    direcao_br = 'down'
    valor_cartao_go = str(valor_cartao_go)[1:]


  cartao = {'valor_br': valor_cartao_br, 'valor_go': valor_cartao_go, 'ultimo_trimestre_go': ultimo_trimestre_go, 'ultimo_trimestre_br': ultimo_trimestre_br, 'direcao_go': direcao_go, 'direcao_br': direcao_br}
  return cartao


series = cath_serie()
dados_cartao = cath_cartoes(series)

desocupacao = {
    'nome': 'Taxa de Desocupação',
    'descricao': 'Variação percentual trimestral',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': dados_cartao['valor_br']+'%',
            'direcao': dados_cartao['direcao_br'],
            'desc_serie': 'Variação percentual trimestral',
            'serie_tipo': 'data',
            'referencia': dados_cartao['ultimo_trimestre_br'],
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
            'valor': dados_cartao['valor_go']+'%',
            'direcao': dados_cartao['direcao_go'],
            'desc_serie': 'Variação percentual trimestral',
            'serie_tipo': 'data',
            'referencia': dados_cartao['ultimo_trimestre_go'],
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
name_json = 'desocupacao'
with open(path_save_json+'desocupacao.json', 'w', encoding='utf-8') as f:
    json.dump(desocupacao, f, ensure_ascii=False, indent=4)

print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')