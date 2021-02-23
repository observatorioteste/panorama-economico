import urllib.parse
import requests
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
from socket import gethostbyname, gaierror
import urllib3
from http.client import RemoteDisconnected 
from functions import *


def min(anos, siglas_N, regiao):
 for sigla_estado in siglas_N:
    for ano in anos:
        estado_nome = sigla_estado
        # ano = '2019'
        
        print("oooooooooooooook")

        row = cath_substancias(regiao, sigla_estado, ano)
        cid = cath_municipios(regiao, sigla_estado, ano)

        cidades = cid.values
        substancias = row.values

        print('Atual:' + sigla_estado)
        url = 'https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx'
        # df_final.iloc[0:0]
        df_final = pd.DataFrame()
        response = cath_requests()
        count = 0

        soup = BeautifulSoup(response.content, 'html5lib')

        data = { tag['name']: tag['value'] 
            for tag in soup.select('input[name^=ctl00]') if tag.get('value')
        }

        state = { tag['name']: tag['value'] 
                for tag in soup.select('input[name^=__]')   
        }

        payload = data.copy()
        payload.update(state)

        payload.update({
            "ctl00$ContentPlaceHolder1$nu_Ano": ano,
            "ctl00$ContentPlaceHolder1$regiao": regiao,
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$regiao",
        })

        response = cath_response(payload)
        soup = BeautifulSoup(response.content, 'html5lib')

        state = { tag['name']: tag['value'] 
                for tag in soup.select('input[name^=__]')
            }

        # payload.pop("ctl00$ContentPlaceHolder1$Estado")
        payload.update(state)
        payload.update({
            "ctl00$ContentPlaceHolder1$Estado": estado_nome,
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$Estado",
        })

        response = cath_response(payload)
        soup = BeautifulSoup(response.content, 'html5lib')


        for cid in cidades:
            for row in substancias:

                subs_ag = row[0]
                municipio_atual = cid[0]
            #     print("############### CONTAGEM: " + str(index) + " ###############")
                print("Cidade:" + cid[1])
                print("Substancia:" + row[1])


                state = { tag['name']: tag['value']
                        for tag in soup.select('input[name^=__]')
                        }

                payload.update(state)
                payload.update({
                    "ctl00$ContentPlaceHolder1$subs_agrupadora": subs_ag,
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$subs_agrupadora"

                })

                response = cath_response(payload)
                soup = BeautifulSoup(response.content, 'html5lib')


                state = { tag['name']: tag['value']
                        for tag in soup.select('input[name^=__]')
                        }

                payload.update(state)
                payload.update({
                    # "ctl00$MainContent$ddlFrom": "01/10/1990 12:00:00 AM",
                    # "ctl00$MainContent$rdoReportFormat": "HTML",
                    "ctl00$ContentPlaceHolder1$Municipio": municipio_atual,
                    "ctl00$ContentPlaceHolder1$rdComparacao": 'dsc_nome_razao',
                    "ctl00$ContentPlaceHolder1$btnGera": "Gera"
                })

                response = cath_response(payload)

                df_list = pd.read_html(response.text)
                df_list = pd.read_html(str(response.text),encoding = 'utf-8', decimal=',', thousands='.')
                df_atual = pd.DataFrame()

                for i, df_atual in enumerate(df_list):
                    df_atual
                    # print(">>>> LEN DF_ATUAL")
                    # len(df_atual)
                # print(df_atual)
                if(len(df_atual) > 1):
                    count = count +1
                    print(len(df_atual))
                    df_atual.drop(["Arrecadador (Empresa)"][0], axis=1)
                    df_atual.columns = df_atual.columns.droplevel()
                    df_atual = df_atual.drop(["Arrecadador (Empresa)"], axis=1)
                    df_atual = df_atual.drop(["Arrecadador (Empresa).1"], axis=1)
                    df_atual.drop(df_atual.tail(1).index,inplace=True) 
                    df_atual.rename(columns={'Arrecadador (Empresa).2': 'Arrecadador (Empresa)'}, inplace = True)
                    df_atual.rename(columns={'% RecolhimentoCFEM': '%RecolhimentoCFEM'}, inplace = True)
                    df_atual = pd.DataFrame(df_atual, columns = ['Arrecadador (Empresa)', 'Qtde Títulos', 'Operação', 'RecolhimentoCFEM', '%RecolhimentoCFEM', 'Cidade', 'Sub_Agrupadoras'])
                    df_atual['Cidade'] = cid[1]
                    df_atual['Estado'] = estado_nome
                    df_atual['Sub_Agrupadoras'] = row[1]
                    df_atual['ano'] = ano
                    df_final = pd.concat([df_final, df_atual])
                    df_final = df_final.reset_index(drop=True)
                    # print('Conteúdo do municipio '+ row[2] + ' armazenado!')
            #         df_final.to_csv('2020_att.csv', encoding ='latin', sep=';')
                    df_final.to_csv('C:/Users/wendelsouza.iel/Documents/mineracao/'+ estado_nome + ano +'.csv', encoding ='latin', sep=';')


#DEU ERRO
# anos = ['2020']
# siglas_N = ['MG']
# regiao = 'SE'
# min(anos, siglas_N, regiao)

anos = ['2020']
siglas_N = ['RS']
regiao = 'S '
min(anos, siglas_N, regiao)

anos = ['2021']
siglas_N = ['MG', 'SP', 'ES']
regiao = 'SE'
min(anos, siglas_N, regiao)

anos = ['2021']
siglas_N = ['BA', 'CE', 'PB', 'PE', 'PI', 'RN', 'SE', 'MA']
regiao = 'NE'
min(anos, siglas_N, regiao)

anos = ['2021']
siglas_N = ['MS']
regiao = 'CO'
min(anos, siglas_N, regiao)

anos = ['2021']
siglas_N = ['SC', 'PR', 'RS']
regiao = 'S '
min(anos, siglas_N, regiao)