import requests
from github import Github
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import numpy as np
from datetime import datetime

url = 'http://www.idealsoftwares.com.br/indices/igp_m.html'
data = requests.get(url)
soup = bs(data.content, "html.parser")


qtd_tables = 2
json_igpm = []
referencia = [None] * qtd_tables
ano = [None] * qtd_tables

for table_num in range(qtd_tables):
  table = soup.find_all('table')
  df = pd.read_html(str(table), decimal=',', thousands='.')[table_num]
  ano[table_num] = df.columns[0][0]
  df.columns = df.columns.droplevel(0)
  # df1['ano']= ano
  df.drop(["Acumulado nos últimos 12 meses %"], axis=1, inplace=True)

  df.rename(columns={'MÊS': 'mes', 'Mensal %': 'mensal', 'Acumulado no ano %': 'acumulado_ano'}, inplace=True)
  
  data = []
  
  for index, row in df.T.iteritems():
    data.append({'acumulado_mes': str(row['acumulado_ano']).replace(".", ","), 'mes': row['mes'], 'mensal': str(row['mensal']).replace(".", ",")})

  json_igpm.append({ano[table_num]: data})


qtd_meses = len(df['mes'])-1

referencia[0] = df['mes'][qtd_meses][:3]+'/'+str(ano[0])
referencia[1] = df['mes'][0][:3]+'/'+str(ano[1])

json_igpm = {
    'igpm_dados': json_igpm,
    'nome_indice': 'Índice Geral de Preços do Mercado - IGP-M',
    'fonte': 'FGV',
    'referencia': str(referencia[1]) + '-' + str(referencia[0]),
    
}

with open('json_igpm.json', 'w', encoding='utf-8') as f:
    json.dump(json_igpm, f, ensure_ascii=False, indent=4)


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


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/igpm.json', 'r', encoding='utf-8') as file:
    content = file.read()
    
# content = content.encode("windows-1252").decode("utf-8")


# Upload to github
git_file = 'panorama-economico/igpm.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')