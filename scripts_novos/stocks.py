import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from datetime import datetime
from github import Github

from upload import *
from util import *

url = 'https://br.investing.com/indices/us-spx-500-futures'


data = {}
sp_future_dic = []
us30_dic = []
sp_vix_dic = []

from datetime import datetime
from pytz import timezone

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
source=requests.get(url, headers=headers).text
soup = BeautifulSoup(source, "html.parser")
data_e_hora_atuais = datetime.now()
fuso_horario = timezone('America/Sao_Paulo')
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M:%S')


sp_future = soup.find(id="sb_last_8839").text
us30 = soup.find(id="sb_last_8873").text
vix = soup.find(id="sb_last_44336").text

sp_future_ant = sp_future
us30_ant = us30
vix_ant = vix

sp_future_dic.append({'S&P 500 Futuros': sp_future, 'data': data_e_hora_sao_paulo_em_texto})
us30_dic.append({'US 30 Futuros': us30, 'data': data_e_hora_sao_paulo_em_texto})
sp_vix_dic.append({'S&P 500 VIX': sp_future, 'data': data_e_hora_sao_paulo_em_texto})

count = 0
while(1):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
  source=requests.get(url, headers=headers).text
  soup = BeautifulSoup(source, "html.parser")
  data_e_hora_atuais = datetime.now()
  fuso_horario = timezone('America/Sao_Paulo')
  data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
  data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M:%S')


  sp_future = soup.find(id="sb_last_8839").text
  us30 = soup.find(id="sb_last_8873").text
  vix = soup.find(id="sb_last_44336").text

  if sp_future != sp_future_ant:
    sp_future_dic.append({'S&P 500 Futuros': sp_future, 'data': data_e_hora_sao_paulo_em_texto})
  
  if us30 != us30_ant:
    us30_dic.append({'US 30 Futuros': us30, 'data': data_e_hora_sao_paulo_em_texto})
  
  if vix_ant != vix:
    sp_vix_dic.append({'S&P 500 VIX': sp_future, 'data': data_e_hora_sao_paulo_em_texto})

  sp_future_ant = sp_future
  us30_ant = us30
  vix_ant = vix
  count +=1

  print({'S&P 500 Futuros': sp_future, 'us30': us30, 'vix': vix})

  if(count > 100):
    # vix = sp_vix_dic
    # sp_future =sp_future_dic
    # us30 = us30_dic

    with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/sp_future.json', 'w', encoding='utf-8') as f:
        json.dump(sp_future_dic, f, ensure_ascii=False, indent=4)
    
    upload_files_to_github('sp_future')
 
    with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/us30.json', 'w', encoding='utf-8') as f:
        json.dump(us30_dic, f, ensure_ascii=False, indent=4)

    upload_files_to_github('us30')
 
    with open('C:/Users/wendelsouza.iel/Desktop/panorama-economico/vix.json', 'w', encoding='utf-8') as f:
        json.dump(sp_vix_dic, f, ensure_ascii=False, indent=4)

    upload_files_to_github('vix')