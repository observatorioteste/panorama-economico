
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date
import util as util
from util import *
from upload import *
from github import Github

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

def cath_referencia(data_ultimo_dado):
  meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
  mes = data_ultimo_dado[5:7]
  ano = data_ultimo_dado[:4]
  print(data_ultimo_dado)
  mes = int(mes)
  if mes == 1: #if igual a janeiro; evita q armazene "jan-jan/2021"
    referencia = (meses_ano[int(mes-1)]+ '/' + ano).capitalize()
  else: 
    referencia = 'Jan-'+(meses_ano[int(mes-1)]+ '/' + ano).capitalize()

  return referencia


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


      valor_br = dados[1]['V']
      mes_referencia = dados[2]['D2N']
      if str(valor_br) != '...':
        referencia_br = mes
        serie_br.append({'x': mes, 'y': float(valor_br)})

      valor_go = dados[2]['V']
      mes_referencia = dados[1]['D2N']
      if str(valor_go) != '...':
        serie_go.append({'x': mes, 'y': float(valor_go)})

    
    except IndexError:
      break

  return {'serie_go': serie_go, 'serie_br': serie_br}      
 
def define_informacoes_cartao(series, serie_escolhida):
  valor_periodo_anterior = series[serie_escolhida][-2:][0]['y']
  valor_periodo_atual = series[serie_escolhida][-2:][1]['y']

  if valor_periodo_atual > 0:
    direcao_seta = 'up'
  elif valor_periodo_atual < 0:
    direcao_seta = 'down'
  else:
    direcao_seta = 'right'

  if valor_periodo_atual >= 0:
    cor_valor = 'green'
    valor_periodo_atual = str(valor_periodo_atual)
  else:
    cor_valor = 'red'
    valor_periodo_atual = str(valor_periodo_atual)[1:]

  referencia = cath_referencia(series['serie_br'][-1:][0]['x'])

  return ({'valor': valor_periodo_atual, 'direcao_seta': direcao_seta,
           'cor_valor': cor_valor, 'referencia': referencia})

series = cath_serie()
cartao_br = define_informacoes_cartao(series, 'serie_br')
cartao_go = define_informacoes_cartao(series, 'serie_go')

inpc_json = {
    'nome': 'Índice Nacional de Preços ao Consumidor - INPC',
    'descricao': 'Variação percentual mensal',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': cartao_br['valor'] +'%',
            'direcao': cartao_br['direcao_seta'],
            'cor_valor': cartao_br['cor_valor'],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartao_br['referencia'],
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
            'valor': cartao_go['valor']+'%',
            'direcao':  cartao_go['direcao_seta'],
            'cor_valor': cartao_go['cor_valor'],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartao_go['referencia'],
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
name_json = 'inpc'

################### Salva o inpc_mesclagem.JSON 
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(inpc_json, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')