#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date

################################## NACIONAL ##############################
# Gera inpc_nacional (JSON)

################### Extração da lista de periodos 
## Formato: 202002 

start = date(2018, 12, 1)
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


################### Extração dos dados
inpc = []
for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/1736/n1/1/p/{0}/v/44/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    serie_json = json.loads(soup.text)
    
    try:
      valor = serie_json[1]['V']
      #add indice na serie
      inpc.append({'mes': mes, 'valor': valor})

    except IndexError:
      break



################### Referencia  
#formato 202011
referencia = inpc[-1:][0]['mes']
valor_cartao = inpc[-1:][0]['valor']

#formato Jan/2020
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

mes_cod = int(str(inpc[-1:][0]['mes'])[-2:])
mes_nome = meses_ano[mes_cod-1]
ano = str(inpc[-1:][0]['mes'])[:4]
referencia_extenso = mes_nome + '/' + ano


################### Criação do JSON - Nacional

json_inpc_nacional = {
    'nome_indice': 'INPC - Índice Nacional de Preços ao Consumidor',
    'fonte': 'SIDRA - IBGE', 
    'referencia': referencia, 
    'referencia_extenso': referencia_extenso,
    'cartao_nacional': valor_cartao,
    'descricao_cartao': 'Variação em relação ao mesmo período do ano anterior',
    'descricao_cartao': "Variação mensal (%)",
    'serie_nacional': inpc,
    'periodicidade': "-",
}


################################## NACIONAL ##############################
# Gera inpc_nacional (JSON)

################### Extração da lista de periodos 
## Formato: 202002 

start = date(2018, 12, 1)
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


################### Extração dos dados
inpc = []
for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/1736/n1/1/p/{0}/v/44/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    pim_federacoes = json.loads(soup.text)
    
    try:
      valor = pim_federacoes[1]['V']
      #add indice na serie
      inpc.append({'mes': mes, 'valor': valor})

    except IndexError:
      break

################### Referencia  
#formato 202011
referencia = inpc[-1:][0]['mes']
valor = inpc[-1:][0]['valor']

#formato Jan/2020
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

mes_cod = int(str(inpc[-1:][0]['mes'])[-2:])
mes_nome = meses_ano[mes_cod-1]
ano = str(inpc[-1:][0]['mes'])[:4]
referencia_extenso = mes_nome + '/' + ano


################### Criação do JSON - Nacional

json_inpc_nacional = {
    'nome_indice': 'INPC - Índice Nacional de Preços ao Consumidor',
    'fonte': 'SIDRA - IBGE', 
    'referencia': referencia, 
    'referencia_extenso': referencia_extenso,
    'cartao_nacional': valor,
    'descricao_cartao': 'Variação em relação ao mesmo período do ano anterior',
    'descricao_cartao': "Variação mensal (%)",
    'serie_nacional': inpc,
    'periodicidade': "-",
}

################################## REGIONAL ##############################
# Gera inpc_regional (JSON)

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

################### Extração da variacao mesmo periodo 
inpc = []
for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/7063/n6/5208707/C315/7169/p/{0}/v/44/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    serie_json = json.loads(soup.text)
    
    try:
      valor = serie_json[1]['V']
      #add indice na serie
      inpc.append({'mes': mes, 'valor': valor})

    except IndexError:
      break

################### Extração variacao mensal

url = 'http://api.sidra.ibge.gov.br/values/t/7063/n6/5208707/C315/7169/p/{0}/v/68/f/u'
url = url.format(referencia)
data = requests.get(url)
soup = bs(data.content, "html5lib")
serie_json = json.loads(soup.text)

try:
  valor_cartao = serie_json[1]['V']

except IndexError:
   valor = '#'   

################### Referencia  
#formato 202011
referencia = inpc[-1:][0]['mes']
valor = inpc[-1:][0]['valor']

#formato Jan/2020
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

mes_cod = int(str(inpc[-1:][0]['mes'])[-2:])
mes_nome = meses_ano[mes_cod-1]
ano = str(inpc[-1:][0]['mes'])[:4]
referencia_extenso = mes_nome + '/' + ano


json_inpc_regional = {
    'nome_indice': 'INPC - Índice Nacional de Preços ao Consumidor',
    'fonte': 'SIDRA - IBGE', 
    'referencia': referencia, 
    'referencia_extenso': referencia_extenso,
    'cartao_regional': valor_cartao,
    'descricao_cartao': 'Variação em relação ao mesmo período do ano anterior',
    'descricao_cartao': "Variação mensal (%)",
    'serie_regional': inpc,
    'periodicidade': "-",
}

 
################################## MESCLAGEM JSON ##############################

inpc_mesclagem = {
    'inpc_nacional': json_inpc_nacional,
    'inpc_regional': json_inpc_regional
}

################### Salva o inpc_mesclagem.JSON 
with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/inpc.json', 'w', encoding='utf-8') as f:
    json.dump(inpc_mesclagem, f, ensure_ascii=False, indent=4)


######################################################
#Upload
g = Github("observatorioteste", "a6beae056fd437a3ceb2bd23f1c4ce8ceb46fe0d")

repo = g.get_user().get_repo('automatizacao_panorama_economico')

all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/inpc.json', 'r', encoding='utf-8') as file:
    content = file.read()
    
# content = content.encode("windows-1252").decode("utf-8")


# Upload to github
git_file = 'panorama-economico/inpc.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')