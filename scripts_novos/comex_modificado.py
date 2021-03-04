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


def direcao_e_cor(serie):
  valor_atual = float(serie[-2:][1]['y'])
  valor_anterior = float(serie[-2:][0]['y'])
  
  if valor_atual > valor_anterior:
    direcao = 'up'
  elif valor_atual < valor_anterior:
    direcao = 'down'
  else:
    direcao = 'right'

  if valor_atual < 0:
      cor_valor = 'red'
      #como o sinal de negativo ('-') não deve aparecer junto ao valor, ele é removido 
      valor_atual = str(valor_atual)[1:] 
  else:
      cor_valor = 'green'
  # else:
  #     cor_valor = 'gray'
  
  return [direcao, valor_atual, cor_valor]

def cath_dados(num_api, num_url, id_serie_target): 
  ###########################################################################
  #CARTAO
  url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/{0}'.format(num_api)
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.content, 'html5lib')
  soup = BeautifulSoup(urlopen(url), "html.parser") 
  all_urls = json.loads(str(soup)) 
  url_page = all_urls['data'][num_url]['url'].replace('http://b', 'https://b')
  
  response = requests.get(url_page, verify=False)
  soup = BeautifulSoup(response.content, 'html5lib')

  importacoes_porcentagem = soup.find_all(class_="count_bottom")[1].text.strip().split("%")[0]
  importacoes_referencia = soup.find_all(class_="count_bottom")[1].text.strip()[-19:]
  exportacoes_porcentagem = soup.find_all(class_="count_bottom")[0].text.strip().split("%")[0]
  exportacoes_referencia = soup.find_all(class_="count_bottom")[0].text.strip()[-19:]

  print('- Dados de extraídos')
  ################### referencia
  exportacoes_referencia = (exportacoes_referencia.replace("  ", " ").replace(exportacoes_referencia[-5:], '').replace(exportacoes_referencia[9:-5], "/"+exportacoes_referencia[10:-5]))[1:]
  importacoes_referencia = (importacoes_referencia.replace("  ", " ").replace(importacoes_referencia[-5:], '').replace(importacoes_referencia[9:-5], "/"+importacoes_referencia[10:-5]))[1:]
  importacoes_referencia = importacoes_referencia.split('. ')[1] #remove "Var." e pega apenas a referencia
  exportacoes_referencia = exportacoes_referencia.split('. ')[1] #remove "Var." e pega apenas a referencia



  ###########################################################################
  #SERIE
  dados_series = soup.select(id_serie_target)
  dados_series = dados_series[0].find('script', type='application/json') 

  now = datetime.now()
  ano_atual = now.year
  ano_anterior = ano_atual - 1

  json_serie_page = json.loads(dados_series.contents[0])
  
  dados_exp = []
  dados_imp = []

  for item in range(len(json_serie_page['x']['data'])):
    ano = int(json_serie_page['x']['data'][item]['CO_ANO'])
    tipo = json_serie_page['x']['data'][item]["TIPO"]
    if (ano == ano_anterior or ano == ano_atual) and tipo == "EXP":
      dados_exp.append(json_serie_page['x']['data'][item])

    if (ano == ano_anterior or ano == ano_atual) and tipo == "IMP":
      dados_imp.append(json_serie_page['x']['data'][item])

  serie_imp = []
  serie_exp = []

  for row in dados_imp:
    if(row['PERIODO'] == 'Total'):
      mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
      # print(row['VL_FOB'])
      fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
      fob = fob +',00'

      serie_imp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})
  
  for row in dados_exp:
    if(row['PERIODO'] == 'Total'):
      mes = pd.to_datetime(row['PERIODO2'], format='%Y-%m-%d', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

      fob = '{:,.0f}'.format(row['VL_FOB']).replace(",",".")
      fob = fob +',00'

      serie_exp.append({'x': mes, 'y': float(row['var_per'][:-1].replace(" ","").replace(",",".")), 'y2': fob})
  
  print('- Série criada')

    #################### Direcao seta
  direcao_imp = direcao_e_cor(serie_imp)
  direcao_exp = direcao_e_cor(serie_exp)
  

  comex_dict = {
      'serie_imp': serie_imp,
      'serie_exp': serie_exp, 
      'direcao_exp': direcao_exp,
      'direcao_imp': direcao_imp,
      'importacoes_porcentagem': importacoes_porcentagem,
      'importacoes_referencia': importacoes_referencia,
      'exportacoes_porcentagem': exportacoes_porcentagem,
      'exportacoes_referencia': exportacoes_referencia,
  }

  return comex_dict

brasil = cath_dados(1, 0, '#série-histórica')
goias = cath_dados(5, 8, '#goiás-série-histórica')

comex_importacao = {
    'nome': 'Importações',
    'descricao': 'Variação em relação ao mesmo mês do ano anterior',
    'fonte': 'MDIC',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(brasil['direcao_imp'][1]) +'%',
            'direcao': brasil['direcao_imp'][0],
            'cor_valor': brasil['direcao_imp'][2],
            'desc_serie': 'Variação percentual em relação ao mesmo período do ano anterior e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': brasil['importacoes_referencia'],
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
            'serie': brasil['serie_imp'],
        },
        {
            'titulo': 'Goiás',
            'valor': str(goias['direcao_imp'][1])+'%',
            'direcao': goias['direcao_imp'][0],
            'cor_valor': goias['direcao_imp'][2],
            'desc_serie': 'Variação percentual em relação ao mesmo período do ano anterior e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': goias['importacoes_referencia'],
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
            'serie': goias['serie_imp'],
        },
    ]
}


comex_exportacao = {
    'nome': 'Exportações',
    'descricao': 'Variação em relação ao mesmo mês do ano anterior',
    'fonte': 'MDIC',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(brasil['direcao_exp'][1]) +'%',
            'direcao': brasil['direcao_exp'][0],
            'cor_valor': brasil['direcao_exp'][2],
            'desc_serie': 'Variação percentual em relação ao mesmo período do ano anterior e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': brasil['exportacoes_referencia'],
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
            'serie': brasil['serie_exp'],
        },
        {
            'titulo': 'Goiás',
            'valor': str(goias['direcao_exp'][1])+'%',
            'direcao': goias['direcao_exp'][0],
            'cor_valor': goias['direcao_exp'][2],
            'desc_serie': 'Variação percentual em relação ao mesmo período do ano anterior e Valor FOB por mês',
            'serie_tipo': 'data',
            'referencia': goias['exportacoes_referencia'],
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
            'serie': goias['serie_exp'],
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


path_save_json = util.config['path_save_json']['path']
name_json = 'comex_exportacao'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(comex_exportacao, f, ensure_ascii=False, indent=4)

######################
#Upload
upload_files_to_github(name_json)
print('- JSONs enviados para o GitHub')
