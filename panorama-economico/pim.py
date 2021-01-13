#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from datetime import datetime


##############################################################################  
#Extração da lista de unidades federativas 
##Formato
#Nome	Código
#Amazonas	13

lista_unidades_fed = pd.read_html('http://api.sidra.ibge.gov.br/LisUnitTabAPI.aspx?c=3653&n=3&i=P')[1]

##############################################################################  
#Extração da lista de periodos 
##Formato: 202002 
data_atual = datetime.today()
qtd_anos_serie = 2
start = datetime((data_atual.year-qtd_anos_serie), 12, 1)
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
    url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/all/p/{0}/v/3140/f/u'
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
brasil = brasil.to_json(orient='records')

pim_nacional_json = {
    'indice': 'PIM_PF_BR',
    'nome': 'Pesquisa Industrial Mensal - Produção Física - PIM PF - Brasil',
    'descricao': 'Variação em relação ao mesmo período do ano anterior',
    'fonte': 'IBGE',
    'referencia': mes_referencia[:3]+ '/' +mes_referencia[-4:], 
    'cartao_nacional': pim_br_indice, 
    'serie_historica_nacional': json.loads(brasil),
    'peridodicidade': 30,
}




# ############# Série histórica regional e índice Goiás ###########

## SERIE HISTORICA >>>> gera serie_hist_regional
serie_hist_regional = []
count = 1
for i, row in lista_unidades_fed.iterrows():
#   print(row[0] + ' (' + str(count) + '/' + str(len(lista_unidades_fed)) + ')')
  count = count + 1
  for mes in lista_periodos:
     
    url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/all/p/{0}/v/3140/N3/{1}/f/u'
    url = url.format(mes, row[1])
    data = requests.get(url)
    soup = bs(data.content, "html5lib")
    pim_federacoes = json.loads(soup.text)
    
    try:
      valor = pim_federacoes[2]['V']
      serie_hist_regional.append({'cod_estado': row[1], 'nome_estado': row[0], 'mes': mes, 'valor': valor})

    except IndexError:
      break


#serie transformada em dataframe
serie_hist_regional_df = pd.DataFrame(serie_hist_regional)

#Indice Goiás >>>>> gera valor_goias_mes_ref
indices_goias = list(serie_hist_regional_df[serie_hist_regional_df['cod_estado'] == 52]['valor'])
indices_goias.reverse()
for ind in indices_goias:
  if ind != '...':
    indice_goias = ind
    break

#Converte dataframe em json
serie_hist_regional_json = serie_hist_regional_df.to_json(orient='records')

#cria json >> gera pim_regional_json
pim_regional_json = {
    'indice': 'PIM_PF_REGIONAL',
    'nome': 'Pesquisa Industrial Mensal - Produção Física - PIM PF - Regional',
    'descricao': 'Variação em relação ao mesmo período do ano anterior',
    'fonte': 'IBGE',
    'referencia': mes_referencia[:3]+ '/' +mes_referencia[-4:], 
    # 'referencia_validacao':  brasil[-1:][0]['mes'],
    'cartao_regional': str(indice_goias)+'%',
    'serie_historica_regional': json.loads(serie_hist_regional_json),
    'peridodicidades': 39
}
 
#cria um json para cada conjunto de dados
pim_regional_json = json.dumps(pim_regional_json)
pim_regional_json = json.loads(pim_regional_json) 

pim_nacional_json = json.dumps(pim_nacional_json)
pim_nacional_json = json.loads(pim_nacional_json) 

#MESCLA OS DOIS JSON >> gera pim
pim = {
    'goias': pim_regional_json,
    'brasil': pim_nacional_json
}

with open('C:/Users/wendelsouza.iel/Desktop/pim.json', 'w', encoding='utf-8') as f:
    json.dump(pim, f, ensure_ascii=False, indent=4)

# value_serializer=lambda pim: json.dumps(pim).encode('utf-8')

# with open('pim.json', 'r') as file:
#     content = file.read()

# with open('data.txt', 'w', encoding='utf-8') as f:
#     json.dump(pim, f, ensure_ascii=False, indent=4)

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


# with open('C:/Users/wendelsouza.iel/Desktop/test.txt', 'r') as file:
#     content = file.read()
# with open('pim.json', 'w') as json_file:
#     json.dump(pim, json_file)

# print(pim)

# with open('pim.txt', 'w') as json_file:
#     json.dump(pim, json_file)

with open('C:/Users/wendelsouza.iel/Desktop/pim.json', 'r') as file:
    content = file.read()
    
content = content.encode("windows-1252").decode("utf-8")

# pim = json.dumps(content)
# content = json.loads(pim) 

 

# Upload to github
# git_prefix = 'folder1/'
# git_file = git_prefix + 'test.txt'
git_file = 'panorama-economico/pim.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="observatorioteste-patch-1")
    print(git_file + ' ATUALIZADO!')
else:
    repo.create_file(git_file, "committing files", content, branch="observatorioteste-patch-1")
    print(git_file + ' CRIADO!')