
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

def cath_referencia(mes):
    if mes[:3] == 'jan':
      mes = 'Jan/'+(str(mes[-4:])).capitalize()
    else:
      mes = 'Jan-'+(mes[:3]+ '/' +mes[-4:]).capitalize()
      
    return mes

def cath_serie():
  serie_go = []
  serie_br = []
  for mes in lista_periodos:
    
    url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/1/p/{0}/v/4139/N3/52/f/u'
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
 
def direcao_seta(series, serie_escolhida):
  valor_periodo_anterior = series[serie_escolhida][-2:][0]['y']
  valor_periodo_atual = series[serie_escolhida][-2:][1]['y']

  if valor_periodo_atual > 0:
    direcao_seta = 'up'
  elif valor_periodo_atual < 0:
    direcao_seta = 'down'
  else:
    direcao_seta = 'right'

  return direcao_seta

def cath_cartao(frederacao):
  
  for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/1/p/{0}/v/3140/N3/52/f/u'
    url = url.format(mes)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)

    try:
      valor = dados[frederacao]['V']
      if str(valor) != '...':
        mes_referencia = dados[1]['D2N']
        ultimo_dado = {'mes': mes_referencia, 'valor': valor}
      
    except IndexError:
      break

  valor_periodo_atual = float(ultimo_dado['valor'])  
  if valor_periodo_atual >= 0:
    cor_valor = 'green'
    valor_periodo_atual = str(valor_periodo_atual)

  else:
    cor_valor = 'red'
    valor_periodo_atual = str(valor_periodo_atual)[1:]  

  ultimo_dado.update({
      'referencia': cath_referencia(ultimo_dado['mes']), 
      'valor': valor_periodo_atual,
      'cor_valor': cor_valor,
  })

  return ultimo_dado  


series = cath_serie()
direcao_br = direcao_seta(series, 'serie_br')
direcao_go = direcao_seta(series, 'serie_go')
cartao_br = cath_cartao(1)
cartao_go = cath_cartao(2)

pim_json = {
    'nome': 'Produção Física Industrial',
    'descricao': 'Variação em relação ao mesmo período do ano anterior (dessasonalizado)',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': cartao_br['valor'] +'%',
            'direcao': direcao_br,
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
            'direcao':  direcao_go,
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
name_json = 'pim'

################### Salva o pim_mesclagem.JSON 
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(pim_json, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')