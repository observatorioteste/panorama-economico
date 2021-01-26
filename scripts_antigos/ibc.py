#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import lxml
import numpy as np


def obtem_ano_anterior(): 
    data_atual = datetime.now()
    ano_anterior = data_atual.year-1
    mes_atual = data_atual.month
    ano_atual = data_atual.year

    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
    url = url.format(ano_anterior, mes_atual, ano_atual)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    data_ibc = json.loads(soup.text)
    ano_anterior = int(data_ibc[-1]['data'][6:10]) - 1
    return str(ano_anterior)



#################################################
#Acesso a API do Governo

data_atual = datetime.now()
ano_anterior = obtem_ano_anterior()
mes_atual = data_atual.month
ano_atual = data_atual.year

url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
url = url.format(ano_anterior, mes_atual, ano_atual)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')
soup = BeautifulSoup(response.content, 'html5lib')

#################################################
#Calculo do índice

data_ibc = json.loads(soup.text)
df_ibc = pd.DataFrame(data_ibc)
df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
df_ibc = df_ibc[['data', 'valor']] 

meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

periodos = list(df_ibc['data'])
valores = list(df_ibc['valor'])

ano = str(periodos[0])[:4]
mes = str(periodos[0])[5:7]

aux = 0
periodos_ext = []
for periodo in periodos:
    mes_do_periodo = meses_ano[int(str(periodo)[5:7])-1]
    periodos[aux] = mes_do_periodo + '/' +(str(periodo))[:4]
    aux = aux + 1
serie_variacao_mensal = {}
for aux in range(len(valores)):
  if(aux < len(valores)-1):
    mes_anterior = float(valores[aux])
    mes_atual = float(valores[aux+1])
    variacao_mensal = (mes_atual/mes_anterior - 1)*100
    serie_variacao_mensal[periodos[aux+1]] = {'variacao_mensal': variacao_mensal}

data_ibc = json.loads(soup.text)
df_ibc = pd.DataFrame(data_ibc)
df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
del df_ibc['data']
test = df_ibc.tail(1)
mes_atualizacao_db = ((test['mes']).astype(int)).tolist()
df_ibc = df_ibc.groupby("ano").head(mes_atualizacao_db)

numero_mes_referencia = int(mes_atualizacao_db[0])
mes_referencia = meses_ano[numero_mes_referencia-1]

ano_ref = np.unique(df_ibc['ano'])[-1]

referencia = 'Jan'+'-'+ mes_referencia + '/' + ano_ref

df_ibc['valor'] = df_ibc['valor'].astype(float)
df_ibc = df_ibc.groupby(['ano']).mean()
df_ibc['valor'][1]/df_ibc['valor'][0]
indice = df_ibc['valor'][1]/df_ibc['valor'][0] -1
indice = indice *100
indice = round(indice,2)



#################################################
#Criação do JSON
ibc_json = {
    'indice': 'IBC-BR',
    'nome': 'Índice de Atividade Econômica do Banco Central (IBC-Br)',
    'descricao_cartao': 'Variação em relação ao mesmo período do ano anterior',
    'fonte': 'IBC',
    'descricao_serie': 'Variação mensal',
    'referencia': referencia, 
    'cartao': str(indice),
    'serie': data_ibc,
    'periodicidade': -
}

# ibc_json = pd.DataFrame(ibc_json)
# ibc_json = ibc_json.to_json(orient='records')

ibc = {
    'ibc': ibc_json,
}


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/ibc.json', 'w', encoding='utf-8') as f:
    json.dump(ibc, f, ensure_ascii=False, indent=4)

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


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/ibc.json', 'r', encoding='utf-8') as file:
    content = file.read()
    
# content = content.encode("windows-1252").decode("utf-8")


# Upload to github
git_file = 'panorama-economico/ibc.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')