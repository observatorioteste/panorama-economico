#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import datetime
import util as util
from util import *
from upload import *


##############################################################################  
#Extração da lista de unidades federativas 
# ##Formato
# #Nome	Código
# #Amazonas	13

# lista_unidades_fed = pd.read_html('http://api.sidra.ibge.gov.br/LisUnitTabAPI.aspx?c=3653&n=3&i=P')[1]

##############################################################################  
#Extração da lista de periodos 
##Formato: 202002 
data_atual = datetime.today()
qtd_anos_serie = 2
ano_extração = data_atual.year-qtd_anos_serie
start = datetime(ano_extração, 12, 1)
end = datetime.today()
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


############################################################################## 
#Dados do Brasil
#gera pim_nacional_json
brasil = []
for mes in lista_periodos:
    url = 'http://https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'/values/t/3653/n1/all/p/{0}/v/3139/f/u'
    url = url.format(mes)
    # print(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    pim_federacoes = json.loads(soup.text)
    
    try:
      valor = pim_federacoes[1]['V']
      brasil.append({'mes': mes, 'valor': valor})
      mes_referencia = pim_federacoes[1]['D2N']
    except IndexError:
      # print(mes)
      break

pim_br_indice = brasil[-1:][0]['valor']
brasil = pd.DataFrame(brasil)
brasil['mes'] = pd.to_datetime(brasil['mes'], format='%Y%m', errors='coerce')
brasil['mes'] = brasil['mes'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
# brasil = brasil.to_json(orient='records')
referencia_br = 'Jan-'+(mes_referencia[:3]+ '/' +mes_referencia[-4:]).capitalize()

#####serie
serie_pim_br = []
for i, row in brasil.iterrows():
  serie_pim_br.append({'x': row[0], 'y': float(row[1])})
#####

print('- Dados (Brasil) foram extraídos')
print('- Série (Brasil) criada')

if float(pim_br_indice) < 0:
  direcao_br = 'down'
  pim_br_indice = str(pim_br_indice)[1:]
else:
  direcao_br = 'up'
  

print('- Valor do cartão (Brasil) foi extraído')

# ############# Série histórica regional e índice Goiás ###########

## SERIE HISTORICA >>>> gera serie_hist_regional
serie_pim_go = []
count = 1

for mes in lista_periodos:
    
  url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/all/p/{0}/v/3139/N3/52/f/u'
  url = url.format(mes)
  data = requests.get(url)
  soup = bs(data.content, "html5lib")
  pim_federacoes = json.loads(soup.text)
  
  try:
    valor = pim_federacoes[2]['V']

    mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")

    serie_pim_go.append({'x': mes, 'y': float(valor)})

  except IndexError:
    break

print('- Dados (Goiás) foram extraídos')
print('- Série (Goiás) foi criada')
#serie transformada em dataframe
serie_hist_regional_df = pd.DataFrame(serie_pim_go)

#Indice Goiás >>>>> gera valor_goias_mes_ref
indices_goias = list(serie_hist_regional_df['y'])
indices_goias.reverse()
for ind in indices_goias:
  if ind != '...':
    pim_go_indice = ind
    break


url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/all/p/last/v/3140/N3/52/f/u'
url = url.format(mes)
data = requests.get(url)
soup = bs(data.content, "html5lib")
cartoes = json.loads(soup.text)
cartao_go = cartoes[2]['V']
cartao_br = cartoes[1]['V']



if float(cartao_br) < 0:
  direcao_br = 'down'
  cartao_br = str(cartao_br)[1:]

else:
  direcao_br = 'up'

if float(cartao_go) < 0:
  direcao_go = 'down'
  cartao_go = str(cartao_go)[1:]

else:
  direcao_go = 'up'



print(cartao_go)





if float(pim_go_indice) < 0:
  direcao_go = 'down'
  pim_go_indice = str(pim_go_indice)[1:]

else:
  direcao_go = 'up'

print('- Valor do cartão (Goiás) foi armazenado')

#MESCLA OS DOIS JSON >> gera pim
pim = {
    'nome': 'Produção Física Industrial',
    'descricao': 'Variação percentual em relação ao mesmo período do ano anterior (dessazonalizado)',
    'fonte': 'IBGE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(cartao_br)+'%',
            'direcao': direcao_br,
            'desc_serie': 'Variação percentual mensal',
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
            'serie': serie_pim_br,
        },
        {
            'titulo': 'Goiás',
            'valor': str(cartao_go)+'%',
            'direcao': direcao_go,
            'desc_serie': 'Variação percentual mensal',
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
            'serie': serie_pim_go,
        }
    ]
}

path_save_json = util.config['path_save_json']['path']
name_json = 'pim'

with open(path_save_json + name_json +'.json', 'w', encoding='utf-8') as f:
    json.dump(pim, f, ensure_ascii=False, indent=4)
print('- JSON foi armazenado')

######################################################
#Upload
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')