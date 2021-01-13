#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import urllib.parse
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


################################## PAGINA GOIAS ##############################
url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/5'
url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/5'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
estados = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json
goias = estados['data'][8]['url']


##################################  CARDS GOAIS ##############################
url = goias
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html5lib')

cards = {}

count = 0
# d = soup.find_all(class_="count_bottom")[0].text.strip().split("%")[]
# d
cards = {
    'exportacoes_absoluto_go': soup.findAll('div', {'class': 'count value'})[0].text.strip(),
    'importacoes_absoluto_go': soup.findAll('div', {'class': 'count value'})[1].text.strip(),
    'corrente_absoluto_go': soup.findAll('div', {'class': 'count value'})[2].text.strip(),
    'saldo_absoluto_go': soup.findAll('div', {'class': 'count value'})[3].text.strip(),
    'exportacoes_porcentagem_go': soup.find_all(class_="count_bottom")[0].text.strip().split("%")[0],
    'importacoes_porcentagem_go': soup.find_all(class_="count_bottom")[1].text.strip().split("%")[0],
    'corrente_porcentagem_go': soup.find_all(class_="count_bottom")[2].text.strip().split("%")[0]
}

################################## SERI GOIAS ##############################
url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/5'

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
estados = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json

goias = estados['data'][8]['url']
html = urlopen(goias)
goias_data = BeautifulSoup(html, 'lxml')
goias_data = goias_data.select('#goiás-série-histórica')
goias_data = goias_data[0].find('script', type='application/json') 

# with open('data_goias.json', 'w') as json_file:
#     json.dump(data_goias, json_file)
# print(goias_data)
json_goias = json.loads(goias_data.contents[0])
# json_goias

################################## JSON GOIAS ##############################
dados_goias = {
    'serie_historica_goias': json_goias,
    'dados_cards_go': cards
}




##################################  CARDS BRASIL ##############################

url = 'http://www.mdic.gov.br/balanca/comex-vis/BrasilGeral/brasil102020.html'
response = requests.get(url)
 
soup = BeautifulSoup(response.content, 'html5lib')

cards = {}

count = 0
# d = soup.find_all(class_="count_bottom")[0].text.strip().split("%")[]
# d
cards = {
    'exportacoes_absoluto_br': soup.findAll('div', {'class': 'count value'})[0].text.strip(),
    'importacoes_absoluto_br': soup.findAll('div', {'class': 'count value'})[1].text.strip(),
    'corrente_absoluto_br': soup.findAll('div', {'class': 'count value'})[2].text.strip(),
    'saldo_absoluto_br': soup.findAll('div', {'class': 'count value'})[3].text.strip(),
    'exportacoes_porcentagem_br': soup.find_all(class_="count_bottom")[0].text.strip().split("%")[0],
    'importacoes_porcentagem_br': soup.find_all(class_="count_bottom")[1].text.strip().split("%")[0],
    'corrente_porcentagem_br': soup.find_all(class_="count_bottom")[2].text.strip().split("%")[0],
}
################################## SERIE BRASIL ##############################

url = 'http://api.comexstat.mdic.gov.br/pt/comex-vis/1'

soup = BeautifulSoup(urlopen(url), "html.parser") #https://stackoverflow.com/questions/25016036/beautifulsoup-soup-body-return-none
brasil_url = json.loads(str(soup)) #https://stackoverflow.com/questions/59665253/how-to-convert-a-beautifulsoup-tag-to-json

brasil_url = brasil_url['data'][0]['url']
brasil_page = urlopen(brasil_url)
brasil_page = BeautifulSoup(brasil_page, 'lxml')
brasil_page = brasil_page.select('#série-histórica')
data_brasil = brasil_page[0].find('script', type='application/json') 

# with open('data_goias.json', 'w') as json_file:
#     json.dump(data_brasil, json_file)

json_brasil = json.loads(data_brasil.contents[0])
# data_brasil

################################## JSON BRASIL ##############################

dados_brasil= {
    'serie_historica_brasil': json_brasil,
    'dados_cards_br': cards,
    'descricao': 'Variação em relação ao mesmo período do ano anterior - Medic',
    'descricao_cards': '"Saldo (US$ Milhões),  Importações (US$ Milhões), Exportações (US$ Milhões), Corrente (US$ Milhões), Importações (%Var), Exportações (%Var), Corrente (%Var)'
}
dados_brasil

# #################################################
#MESCLAGEM JSON

json_comex = comex_completo = {
    'dados_brasil':dados_brasil,
    'dados_goias':dados_goias
}


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/comex.json', 'w', encoding='utf-8') as f:
    json.dump(json_comex, f, ensure_ascii=False, indent=4)


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


with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/comex.json', 'r', encoding='utf-8') as file:
    content = file.read()
    
# content = content.encode("windows-1252").decode("utf-8")


# Upload to github
git_file = 'panorama-economico/comex.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')