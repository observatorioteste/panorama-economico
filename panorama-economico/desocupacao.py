#!/usr/bin/env python
# coding: utf-8

# BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import date 
import util as f

# test = f.config['repositorio-name']['repositorio']
print(f.config['repositorio-name']['repositorio'])



#################################################
#federacoes
lista_unidades_fed = pd.read_html('http://api.sidra.ibge.gov.br/LisUnitTabAPI.aspx?c=4099&n=3&i=P')[1]


#################################################


url = 'http://api.sidra.ibge.gov.br/desctabapi.aspx?c=4099'
data = requests.get(url)
soup = bs(data.content, "html.parser")
periodos = soup.find(id="lblPeriodoDisponibilidade").get_text(strip=True)

lista_periodos = []
periodos = periodos.strip(',').split(', ') 
trimestre_base = 201901

for i in range(len(periodos)):
  trimestre = int(periodos[i])
  if trimestre >= trimestre_base:
    lista_periodos.append(trimestre)


################################## DADOS DO BRASIL ##############################
taxas_brasil = []
for mes in lista_periodos:
    # print(mes)
    url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n1/1/p/{0}/f/u'
    url = url.format(mes)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    taxa = json.loads(soup.text)
    
    try:
      valor = taxa[1]['V']
      taxas_brasil.append({'mes': mes, 'valor': valor})

    except IndexError:
      break

brasil = {
    'serie': taxas_brasil
}

#Ultima taxa nacional
url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n1/1/p/last/f/u'
data = requests.get(url)
soup = bs(data.content, "html5lib")
data_brasil_ultimo = json.loads(soup.text)

referencia_br  = data_brasil_ultimo[1]['D3N']
indice_brasil_ultimo = data_brasil_ultimo[1]['V']
 


################################## GOIAS ##############################

taxas_por_federacao = []
count = 1
for i, row in lista_unidades_fed.iterrows():
#   print(row[0] + ' (' + str(count) + '/' + str(len(lista_unidades_fed)) + ')')
  count = count + 1
  for trimestre in lista_periodos:
     
    url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n3/{0}/p/{1}/f/u'
    url = url.format(row[1],trimestre)
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    taxas_json = json.loads(soup.text)
    
    try:
      taxa = taxas_json[1]['V']
      taxas_por_federacao.append({'cod_estado': row[1], 'nome_estado': row[0], 'mes': trimestre, 'valor': taxa})
    except IndexError:
      print('Indexação incorreta! Verificar: taxas_json[1][]')
      break

taxas_por_federacao = pd.DataFrame(taxas_por_federacao)
taxas_por_federacao = taxas_por_federacao.to_json(orient='records')
taxas_por_federacao = json.loads(taxas_por_federacao)

#ultima taxa de goias
url = 'http://api.sidra.ibge.gov.br/values/t/4099/v/4099/n3/52/p/last/f/u'
data = requests.get(url)
soup = bs(data.content, "html5lib")
data_goias = json.loads(soup.text)

referencia_go = data_brasil_ultimo[1]['D3N']
indice_goias_ultimo = data_goias[1]['V']

#################################################
#Criação do JSON
json_desocupacao_regional = {
    'indice': 'taxa_de_desocupacao_go',
    'cartao_regional': indice_goias_ultimo,
    'referencia': referencia_go,
    'serie_goias': taxas_por_federacao,
    'descricao': 'Percentual no trimestre (IBGE)',
}

json_desocupacao_nacional = {
    'indice': 'taxa_de_desocupacao_br',
    'cartao_nacional': indice_brasil_ultimo,
    'referencia': referencia_br,
    'descricao': 'Percentual no trimestre (IBGE)',
    'serie_brasil': taxas_brasil,
}

desocupacao_mesclagem = {
    'desocupacao_nacional': json_desocupacao_nacional,
    'desocupacao_regional': json_desocupacao_regional
}

with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/desocupacao.json', 'w', encoding='utf-8') as f:
    json.dump(desocupacao_mesclagem, f, ensure_ascii=False, indent=4)


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


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/desocupacao.json', 'r', encoding='utf-8') as file:
    content = file.read()
    
# content = content.encode("windows-1252").decode("utf-8")


# Upload to github
git_file = 'panorama-economico/desocupacao.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')