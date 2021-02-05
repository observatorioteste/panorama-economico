import requests

def cath_response(payload):
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
    
    url = "https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx"

    while 1:    
        try:
            response = requests.post(url, data=payload, allow_redirects=True)
            break

        except RemoteDisconnected as e:
            print(' ')
            print('errro resp - RemoteDisconnected...')
            print(' ')
            time.sleep(400)
            continue        

        except urllib3.exceptions.ProtocolError as e:
            print(' ')
            print('errro resp - ProtocolError...')
            print(' ')
            time.sleep(400)
            continue
        
        except (requests.exceptions.ConnectionError, ConnectionError) as e:
            print(' ')
            print('errro resp - ConnectionError...')
            print(' ')
            time.sleep(400)
            continue
        
    return response

def cath_requests():
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
    
    url = "https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx"

    while 1:    
        try:
            response = requests.get(url) 
            break

        except RemoteDisconnected as e:
            print(' ')
            print('erro resp - RemoteDisconnected...')
            print(' ')
            time.sleep(500)
            continue        

        except urllib3.exceptions.ProtocolError as e:
            print(' ')
            print('erro resp - ProtocolError...')
            print(' ')
            time.sleep(500)
            continue
        
        except (requests.exceptions.ConnectionError, ConnectionError) as e:
            print(' ')
            print('erro resp - ConnectionError...')
            print(' ')
            time.sleep(500)
            continue
        
    return response

      



def cath_substancias(regiao, estado_nome, ano):
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

    regiao = regiao
    estado_nome = estado_nome
    ano = ano

    url = 'https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx'
    # df_final.iloc[0:0]
    df_final = pd.DataFrame()
    response = cath_requests()
    count = 0

    # soup = BeautifulSoup(response.content, 'html5lib')
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html5lib')

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

    # print("Cidade:" + cid[1])
    # print("Substancia:" + row[1])

    state = { tag['name']: tag['value']
        for tag in soup.select('input[name^=__]')
    }

    payload.update(state)
    # payload.update({
    #     "ctl00$ContentPlaceHolder1$subs_agrupadora": subs_ag,
    #     "__EVENTTARGET": "ctl00$ContentPlaceHolder1$subs_agrupadora"
    # })

    response = cath_response(payload)
    soup = BeautifulSoup(response.content, 'html5lib')

    state = { tag['name']: tag['value']
        for tag in soup.select('input[name^=__]')
    }

    payload.update(state)
    payload.update({
    #     "ctl00$ContentPlaceHolder1$Municipio": municipio_atual,
        "ctl00$ContentPlaceHolder1$rdComparacao": 'SuAg_Nome_Subst_Agrupadora',
        "ctl00$ContentPlaceHolder1$btnGera": "Gera"
    })

    response = cath_response(payload)
    
    df_list = pd.read_html(response.text)
    df_list = pd.read_html(str(response.text),encoding = 'utf-8', decimal=',', thousands='.')
    substancias_estado_df = pd.DataFrame()

    for i, substancias_estado_df in enumerate(df_list):
        substancias_estado_df

    substancias_estado_df.drop(["Arrecadador (Subs. Agrupadora)"][0], axis=1)
    substancias_estado_df.columns = substancias_estado_df.columns.droplevel()
    substancias_estado_df = substancias_estado_df.drop(["Arrecadador (Subs. Agrupadora)"], axis=1)
    substancias_estado_df = substancias_estado_df.drop(["Arrecadador (Subs. Agrupadora).1"], axis=1)
    substancias_estado_df.drop(substancias_estado_df.tail(1).index,inplace=True) 
    substancias_estado_df.rename(columns={'Arrecadador (Subs. Agrupadora).2': 'substancia'}, inplace = True)
    substancias_estado_df = substancias_estado_df.drop(["Qtde Títulos", "Operação", "RecolhimentoCFEM", "% RecolhimentoCFEM"], axis=1)
    
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
    tables = soup.select('#ctl00_ContentPlaceHolder1_subs_agrupadora')

    todas_substancias = []

    for option in tables[0].find_all('option')[1:]:    
        todas_substancias.append({'value': option['value'], 'substancia': option.text})
                                
    todas_substancias_df = pd.DataFrame.from_dict(todas_substancias, orient='columns')
    

    df_final = substancias_estado_df.merge(todas_substancias_df, on='substancia')
    df = pd.DataFrame()
    df['value'] = df_final['value']
    df['municipios'] = df_final['substancia']

    return df

def cath_municipios(regiao, estado_nome, ano):

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

    regiao = regiao
    estado_nome = estado_nome
    ano = ano

    url = 'https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx'
    # df_final.iloc[0:0]
    df_final = pd.DataFrame()
    response = cath_requests()
    count = 0

    # soup = BeautifulSoup(response.content, 'html5lib')
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html5lib')

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

    # print("Cidade:" + cid[1])
    # print("Substancia:" + row[1])

    state = { tag['name']: tag['value']
        for tag in soup.select('input[name^=__]')
    }

    payload.update(state)

    response = cath_response(payload)
    soup = BeautifulSoup(response.content, 'html5lib')

    state = { tag['name']: tag['value']
        for tag in soup.select('input[name^=__]')
    }

    payload.update(state)
    payload.update({
    #     "ctl00$ContentPlaceHolder1$Municipio": municipio_atual,
        "ctl00$ContentPlaceHolder1$rdComparacao": "muni_nome_municipio + ' - ' + boleto_pago.unfe_sigla_uf",
        "ctl00$ContentPlaceHolder1$btnGera": "Gera"
    })

    response = cath_response(payload)

    df_list = pd.read_html(response.text)
    df_list = pd.read_html(str(response.text),encoding = 'utf-8', decimal=',', thousands='.')
    municipios_df = pd.DataFrame()

    for i, municipios_df in enumerate(df_list):
        municipios_df

    municipios_df.drop(["Arrecadador (Município)"][0], axis=1)
    municipios_df.columns = municipios_df.columns.droplevel()
    municipios_df = municipios_df.drop(["Arrecadador (Município)"], axis=1)
    municipios_df = municipios_df.drop(["Arrecadador (Município).1"], axis=1)
    municipios_df.drop(municipios_df.tail(1).index,inplace=True) 
    municipios_df.rename(columns={'Arrecadador (Município).2': 'municipios'}, inplace = True)
    municipios_df = municipios_df.drop(["Qtde Títulos", "Operação", "RecolhimentoCFEM", "% RecolhimentoCFEM"], axis=1)

    for index in municipios_df.index:
        municipios_df['municipios'][index]  =  municipios_df['municipios'][index].replace(' - '+estado_nome, '')

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
    tables = soup.select('#ctl00_ContentPlaceHolder1_Municipio')
    
    todos_municipios = []

    for option in tables[0].find_all('option')[1:]:    
        todos_municipios.append({'value': option['value'], 'municipios': option.text})
                                
    todos_municipios_df = pd.DataFrame.from_dict(todos_municipios, orient='columns')

    df_final = municipios_df.merge(todos_municipios_df, on='municipios')
    df = pd.DataFrame()
    df['value'] = df_final['value']
    df['municipios'] = df_final['municipios']

    return df