# Import packages
import os 
import pickle
import configparser

# Load config
config = configparser.ConfigParser()


if 'config.example.ini' in os.listdir():
    config.read('config.example.ini')
else:
    config.read('../config.example.ini')

if 'config.ini' in os.listdir():
    config.read('config.ini')
else:
    config.read('../config.ini')


##############################################
FONTE_IGPM = 'http://www.idealsoftwares.com.br/indices/igp_m.html' 
# FONTE_DESOCUPACAO = 'http://api.sidra.ibge.gov.br/LisUnitTabAPI.aspx?c=4099&n=3&i=P'

##################################### DIREÇÃO

def direcao_zero(valor):
    if float(valor) < 0:
        direcao = 'down'
        valor = valor[1:]
    else:
        direcao = 'up'
    
    return [direcao, valor]