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
            
#################################################
#Extração dos dados
#Conectando-se ao endereço
ftp = ftplib.FTP("ftp.mtps.gov.br")
ftp.login()
ftp.encoding = "LATIN-1"

#Local de salvamento do arquivos compactados
caminho_pasta_compactados = 'G:/IEL/ATENDIMENTO AO CLIENTE WEB 2021/00000 PLANEJAMENTO DESENV EMPRESARIAL 2021/0000 PLANEJAMENTO ESTUDOS E PESQUISAS 2021-IEL-SANDRA/OBSERVATÓRIO/ATUALIZAÇÃO DE DADOS/panorama economico wendel/caged wendel/compactados/'
caminho_pasta_extracao = 'G:/IEL/ATENDIMENTO AO CLIENTE WEB 2021/00000 PLANEJAMENTO DESENV EMPRESARIAL 2021/0000 PLANEJAMENTO ESTUDOS E PESQUISAS 2021-IEL-SANDRA/OBSERVATÓRIO/ATUALIZAÇÃO DE DADOS/panorama economico wendel/caged wendel/extraidos/'

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
         
        # nomes_arquivos = recuperaNomesArquivos()
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        for arquivo in nomes_arquivos:
            # getFile(ftp, caminho_pasta_compactados, arquivo)
            # path_zip = caminho_pasta_compactados + arquivo 
            # # Archive(path_zip).extractall(caminho_pasta_extracao)
            
            # shutil.unpack_archive(path_zip, caminho_pasta_extracao)
            # print(arquivo)

            mes = arquivo[:-3]
            mes = mes[8:]
            movimentacao = manipulacao_movimentacao(caminho_pasta_extracao, arquivo)
            movimentacao_total[mes] = movimentacao
        
            count_mov = count_mov + 1 
            del movimentacao

        print("Os dados foram salvos com sucesso!")
        break
        
ultimo_mes = list(movimentacao_total.keys())[-1]
mov_br = movimentacao_total[ultimo_mes]['movimentacao_br']
mov_go = movimentacao_total[ultimo_mes]['movimentacao_go']

#################################################
#Criação do JSON
caged_json = {
    'indice': 'NOVO CAGED',
    'nome': 'Cadastro Geral de Empregados e Desempregados - CAGED',
    'descricao': '-',
    'fonte': 'Ministério do Trabalho',
    'referencia': ultimo_mes, 
    'saldo_ultimo_mes_br': mov_br,
    'saldo_ultimo_mes_go': mov_go,
    'periodicidade': 'mensal',
}

caged_json = {
    'novo_caged': caged_json,
}

path_save_json = util.config['path_save_json']['path']
name_json = 'novo_caged'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(caged_json, f, ensure_ascii=False, indent=4)


upload_files_to_github(name_json)
print("Atualizado!")