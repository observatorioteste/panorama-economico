#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import date
import lxml
import numpy as np
import csv
import os    
import urllib.parse
import numpy as np
import json
import ftplib
import patoolib
from urllib.request import urlopen
from pyunpack import Archive
from py7zr import unpack_7zarchive
import shutil
import util as util
from util import *
from upload import *


#################################################
#Funcoes

def getFile(ftp, path, filename):
    try:
        file_content =  open(path + filename, 'wb')
        ftp.retrbinary("RETR " + filename, file_content.write)
        file_content.close()
    except:
        print("Error")

def recuperaNomesArquivos():

    meses_dos_arquivos = []
    
    try:
        ftp = ftplib.FTP("ftp.mtps.gov.br")
        ftp.login()
        ftp.encoding = "LATIN-1"
        ftp.cwd('pdet/microdados/NOVO CAGED/Movimentações/2020')
        meses_dos_arquivos = ftp.nlst()
    except ftplib.error_perm:
        if str(resp) == "550 No files found":
            pass
        else:
            raise
    
    return meses_dos_arquivos        

def manipulacao_movimentacao(caminho_pasta_extracao, arquivo):
    mov = {}
    print('- Dados foram extraídos')
    df= pd.read_csv(caminho_pasta_extracao+arquivo[:-3]+'.txt', delimiter=';')
    
    
    df.drop(['região', 'subclasse', 'cbo2002ocupação', 'categoria',
           'graudeinstrução', 'idade', 'horascontratuais', 'raçacor', 'sexo',
           'tipoempregador', 'tipoestabelecimento', 'tipodedeficiência',
           'indtrabintermitente', 'indtrabparcial', 'salário', 'tamestabjan',
           'fonte'
           ], axis=1, inplace = True)  
    
    mask = ((df['seção'] != 'C'))
    df = df.loc[~mask]

    movimentacao = list(df['saldomovimentação'])
    mov_br = calcula_movimentacao(movimentacao)
    
    mask = ((df['uf'] != 52) | (df['seção'] != 'C'))
    df = df.loc[~mask]
    movimentacao = list(df['saldomovimentação'])
    mov_go = calcula_movimentacao(movimentacao)
    df = pd.DataFrame()    
    del mask
    del movimentacao
    print('- Saldo parcial foi calculado')
    return {'movimentacao_br': mov_br, 'movimentacao_go': mov_go}
     
def calcula_movimentacao(mov):
    admissoes = 0 
    desligamentos = 0
    for i in mov:
        if(i == 1):
            admissoes = admissoes + i
        else:
            desligamentos = desligamentos + i
            
    return {'saldo': admissoes-(desligamentos*(-1)), 'desligamentos': desligamentos, 'admissoes': admissoes}

def muda_formato_data(data):
    mes = data
    mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
    return mes            
#################################################
#Extração dos dados
#Conectando-se ao endereço
ftp = ftplib.FTP("ftp.mtps.gov.br")
ftp.login()
ftp.encoding = "LATIN-1"
print('- FTP acessado')

#Local de salvamento do arquivos compactados
caminho_pasta_compactados = 'C:/Users\wendelsouza.iel/Desktop/compactados/'
caminho_pasta_extracao = 'C:/Users/wendelsouza.iel/Desktop/extraidos/'

#Data sobre a data atual de exercução
today = date.today()
mes_atual = today.year
mes_atual = today.month - 1 #menos 1 por causa do indice da lista que começa em zero

meses_ano = ['Dezembro','Novembro','Outubro','Setembro','Agosto','Julho',
         'Junho','Maio','Abril','Março','Fevereiro','Janeiro']

#Recupera os nomes dos arquivos
meses_dos_arquivos = recuperaNomesArquivos()

movimentacao_total = {}
count_mov = 0

#Roda "meses_ano" de trás para frente e baixa os arquivos do último mês
for mes in meses_ano:    
    if mes in meses_dos_arquivos:
        path_dir = '/pdet/microdados/NOVO CAGED/Movimentações/2020/' + mes +'/'
        ftp.cwd(path_dir)
        nomes_arquivos =ftp.nlst()        
        
        print('- Download .ZIP e tranformação para .TXT')
        # nomes_arquivos = recuperaNomesArquivos()
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        for arquivo in nomes_arquivos:
            
            getFile(ftp, caminho_pasta_compactados, arquivo)
            path_zip = caminho_pasta_compactados + arquivo 
            # Archive(path_zip).extractall(caminho_pasta_extracao)
            
            shutil.unpack_archive(path_zip, caminho_pasta_extracao)  

            print('- '+ arquivo)

            mes = arquivo[:-3]
            mes = mes[8:]
            movimentacao = manipulacao_movimentacao(caminho_pasta_extracao, arquivo)
            movimentacao_total[mes] = movimentacao
            # print(arquivo)
            count_mov = count_mov + 1 
            del movimentacao

        print("- Os dados foram salvos com sucesso")
        break
print(movimentacao_total)
print('\n')        
print('- Saldo total calculado')
ultimo_mes = list(movimentacao_total.keys())[-1]
referencia = ultimo_mes
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
referencia = str(referencia)[:7]
mes_cod = int(referencia[4:])
mes_nome = meses_ano[mes_cod-1]
ano = str(referencia[:4])
referencia_br = mes_nome + '/' + ano

mov_br = movimentacao_total[ultimo_mes]['movimentacao_br']
mov_go = movimentacao_total[ultimo_mes]['movimentacao_go']

ultimo_mes = list(movimentacao_total.keys())[-1]
penultimo_mes = list(movimentacao_total.keys())[-2]

# valor_direcao_br = movimentacao_total[ultimo_mes]['movimentacao_br']['saldo'] - movimentacao_total[penultimo_mes]['movimentacao_br']['saldo']
# valor_direcao_go = movimentacao_total[ultimo_mes]['movimentacao_go']['saldo'] - movimentacao_total[penultimo_mes]['movimentacao_go']['saldo']
# print(movimentacao_total[ultimo_mes]['movimentacao_go']['saldo'] )
# print(movimentacao_total[penultimo_mes]['movimentacao_go']['saldo'])
# print('-')
valor_direcao_br = movimentacao_total[ultimo_mes]['movimentacao_br']['saldo']
valor_direcao_go = movimentacao_total[ultimo_mes]['movimentacao_go']['saldo']

valor_direcao_br = str(valor_direcao_br)
valor_direcao_go = str(valor_direcao_go)

if int(valor_direcao_br) < 0:
    direcao_br = 'down'
    valor_direcao_br = valor_direcao_br[1:]
else:
    direcao_br = 'up'

if int(valor_direcao_go) <0:
    direcao_go = 'down'
    valor_direcao_go = valor_direcao_go[1:]
else:
    direcao_go = 'up'

print('- Valores do cartão foram armazenados')

#################################################
#Criação do JSON

if mov_go['saldo'] < 0:
    valor_go = str(mov_go['saldo'])
    valor_go = int(valor_go[1:])
else:
    valor_go = int(mov_go['saldo'])

if mov_br['saldo'] < 0:
    valor_br = str(mov_br['saldo'])
    valor_br = int(valor_br[1:])
else:
    valor_br = int(mov_br['saldo'])

serie_go = []
serie_br = []
for key, value in movimentacao_total.items():
    mes = muda_formato_data(key)
    
    saldo_go = value['movimentacao_go']['saldo']
    serie_go.append({'x': mes, 'y': saldo_go})
    
    saldo_br = value['movimentacao_br']['saldo']
    serie_br.append({'x': mes, 'y': saldo_br})


caged_json = {
    'nome': 'Saldo de Empregados da Ind. de Transformação',
    'descricao': 'Saldo de empregados = Admitidos - Desligados',
    'fonte': 'CAGED',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': valor_br,
            'direcao': direcao_br,
            'referencia': referencia_br,
            'desc_serie': 'Saldo de empregados por mês',
            'serie_tipo': 'data',
            'y_label':{
                'prefixo_sufixo':'sufixo',
                'label':'',
            },
            'serie_labels':{
                'x': 'Data',
                'y': 'Valor'
            },
            'serie': serie_br,
        },
        {
            'titulo': 'Goiás',
            'valor': valor_go,
            'direcao': direcao_go,
            'referencia': referencia_br,
            'desc_serie': 'Saldo de empregados por mês',
            'serie_tipo': 'data',
            'y_label':{
                'prefixo_sufixo':'sufixo',
                'label':'',
            },
            'serie_labels':{
                'x': 'Data',
                'y': 'Valor'
            },
            'serie': serie_go,
        },
    ]
}

path_save_json = util.config['path_save_json']['path']
name_json = 'saldo_desemprego_caged'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(caged_json, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')