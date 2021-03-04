#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import datetime
import lxml
import numpy as np
import util as util
from util import *
from upload import *
from github import Github


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

      valor_br = dados[1]['V']

      if str(valor_br) != '...':
        ultimo_trimestre_br = dados[1]['D2N'][:1]
        trimestre_referencia = dados[2]['D2N']
        trimestre_referencia = cath_trimestre(trimestre_referencia)
        serie_br.append({'x': trimestre_referencia, 'y': float(valor_br)})

      valor_go = dados[2]['V']      

      if str(valor_go) != '...':
        ultimo_trimestre_go = dados[1]['D2N'][:1]
        trimestre_referencia = dados[1]['D2N']
        trimestre_referencia = cath_trimestre(trimestre_referencia)

        serie_go.append({'x': trimestre_referencia, 'y': float(valor_go)})



    except IndexError:
      break

  return {'serie_go': serie_go, 'serie_br': serie_br, 'ultimo_trimestre_br': ultimo_trimestre_br, 'ultimo_trimestre_go': ultimo_trimestre_go}     

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
      valor_atual = str(valor_atual)
      cor_valor = 'green'
  # else:
  #     cor_valor = 'gray'
  
  return {'direcao': direcao, 'valor_atual': valor_atual, 'cor_valor': cor_valor}

def cath_cartoes(series):

  trimestre_para_cartao = {'1': 'Jan-Mar/', '2': 'Abr-Jun/', '3': 'Jul-Set/', '4': 'Out-Dez/'}
  valor_periodo_atual_go = str(series['serie_go'][-1:][0]['y'])
  valor_periodo_atual_br = str(series['serie_br'][-1:][0]['y'])
  valor_cartao_go = valor_periodo_atual_go
  valor_cartao_br = valor_periodo_atual_br
  valor_periodo_anterior_go = str(series['serie_go'][-2:][0]['y'])
  valor_periodo_anterior_br = str(series['serie_br'][-2:][0]['y'])
  ano_go = series['serie_go'][-1:][0]['x'][:4]
  ano_br = series['serie_go'][-1:][0]['x'][:4]
  ultimo_trimestre_go = trimestre_para_cartao[series['ultimo_trimestre_go']] + ano_go
  ultimo_trimestre_br = trimestre_para_cartao[series['ultimo_trimestre_br']] + ano_br
  # print(valor_periodo_anterior_br, valor_periodo_anterior_go)
  # print(valor_periodo_atual_br, valor_periodo_atual_go)
  # direcao_br = direcao_seta(valor_periodo_anterior_br, valor_periodo_atual_br)
  # direcao_go = direcao_seta(valor_periodo_anterior_go, valor_periodo_atual_go)
  direcao_br = direcao_e_cor(series['serie_br'])
  direcao_go = direcao_e_cor(series['serie_go'])
  print(direcao_go)
  cartao = {'valor_br': direcao_br['valor_atual'], 'valor_go': direcao_go['valor_atual'], 'ultimo_trimestre_go': ultimo_trimestre_go, 
            'ultimo_trimestre_br': ultimo_trimestre_br, 'direcao_go': direcao_go['direcao'], 'direcao_br': direcao_br['direcao'],
            'cor_valor_go': direcao_go['cor_valor'], 'cor_valor_br': direcao_br['cor_valor'],
            
            
            }
  return cartao

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
            'cor_valor': dados_cartao['cor_valor_br'],
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
            'cor_valor': dados_cartao['cor_valor_go'],
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
print(' JSON armazenado')

######################################################
#Upload
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')

# def obtem_ano_anterior(): 
#     data_atual = datetime.now()
#     ano_anterior = data_atual.year-1
#     mes_atual = data_atual.month
#     ano_atual = data_atual.year

#     url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
#     url = url.format(ano_anterior, mes_atual, ano_atual)

#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html5lib')
#     soup = BeautifulSoup(response.content, 'html5lib')
#     data_ibc = json.loads(soup.text)
#     ano_anterior = int(data_ibc[-1]['data'][6:10]) - 1
#     return str(ano_anterior)

# #################################################
# #Acesso a API do Governo

# data_atual = datetime.now()
# ano_anterior = str(int(obtem_ano_anterior()) - 1)
# mes_atual = data_atual.month
# ano_atual = data_atual.year

# url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
# url = url.format(ano_anterior, mes_atual, ano_atual)

# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html5lib')
# data_ibc = json.loads(soup.text)
# df_ibc = pd.DataFrame(data_ibc)
# print('- Dados extraídos')
# #################################################


# df_ibc["valor"] = pd.to_numeric(df_ibc["valor"])


# shifted = df_ibc['valor'].shift(1) #realiza o deslocamento de linhas (desloca uma linha)
# df_ibc['variacao_mensal'] = ((df_ibc['valor'] - shifted) / shifted)*100

# df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
# df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
# df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
# df_ibc = df_ibc[['data', 'variacao_mensal']] 

# df_ibc['data'] = df_ibc['data'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
# df_ibc = df_ibc[-24:]

# #####serie
# serie_ibc = []
# for i, row in df_ibc.iterrows():
#   if row[0][:4] >= '2020':
#     serie_ibc.append({'x': row[0], 'y': round(float(row[1]), 2)})
# #####


# meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# print('Série criada')

# periodos = list(df_ibc['data'])
# valores = list(df_ibc['variacao_mensal'])
# ano = str(periodos[0])[:4]
# mes = str(periodos[0])[5:7]


# data_ibc = json.loads(soup.text)
# df_ibc = pd.DataFrame(data_ibc)
# df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
# df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
# df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
# del df_ibc['data']
# test = df_ibc.tail(1)
# mes_atualizacao_db = ((test['mes']).astype(int)).tolist()
# df_ibc = df_ibc.groupby("ano").head(mes_atualizacao_db)

# numero_mes_referencia = int(mes_atualizacao_db[0])
# mes_referencia = meses_ano[numero_mes_referencia-1]

# ano_ref = np.unique(df_ibc['ano'])[-1]

# referencia = mes_referencia + '/' + ano_ref


# df_ibc['valor'] = df_ibc['valor'].astype(float)
# df_ibc = df_ibc.groupby(['ano']).mean()
# #variacao = ((soma_periodo_anterir/ soma_periodo_atual) -1) /100
# indice = (df_ibc['valor'][2]/df_ibc['valor'][1] -1 )*100 
# indice = round(indice,2)
               
# if indice < 0:
#   indice = str(indice)[1:]
#   cor_valor = "red"
# else:
#   indice = str(indice)
#   cor_valor = "green"

# valor_periodo_atual = serie_ibc[-2:][1]['y']
# valor_periodo_anterior = serie_ibc[-2:][0]['y']

# if valor_periodo_atual > 0:
#   direcao = 'up'
# elif valor_periodo_atual < 0:
#   direcao = 'down'
# else:
#   direcao = 'right'

# print('- Valor do cartão armazenado')
# #################################################
# #Criação do JSON
# ibc_json = {
#     'nome': 'Índice de Atividade Econômica',
#     'descricao': 'Variação percentual em relação ao mesmo período do ano anterior (dessazonalizado)',
#     'fonte': 'BACEN',
#     'stats': [
#         {
#             'titulo': 'Brasil',
#             'valor': indice+'%',
#             'direcao': direcao,
#             'cor_valor': cor_valor,
#             'desc_serie': 'Variação percentual mensal',
#             'serie_tipo': 'data',
#             'referencia': 'Jan-' + referencia,
#             'y_label': {
#                     'prefixo_sufixo': 'sufixo',
#                     'label': '%',
#             },
#             'serie_labels': {
#                 'x': 'Data',
#                 'y': 'Variação'
#             },
#             'serie': serie_ibc,
#         }
#     ]
# }

# path_save_json = util.config['path_save_json']['path']

# with open(path_save_json+'ibc.json', 'w', encoding='utf-8') as f:
#     json.dump(ibc_json, f, ensure_ascii=False, indent=4)

# print(' JSON armazenado')

# ######################################################
# #Upload
# upload_files_to_github('ibc')
# print('- JSON enviado para o GitHub')