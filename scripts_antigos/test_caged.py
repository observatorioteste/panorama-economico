# import csv
# import os    
# import urllib.parse
# import requests
# import numpy as np
# import json
# import ftplib
# import patoolib
# from bs4 import BeautifulSoup
# from urllib.request import urlopen
# import pandas as pd
# from datetime import date
# from pyunpack import Archive
# from sys import getsizeof
# from pandas import DataFrame


# import io

# caminho_pasta_extracao = 'G:/IEL/ATENDIMENTO AO CLIENTE WEB 2020/00000 PLANEJAMENTO DESENV EMPRESARIAL 2020/00003 PLANEJAMENTO ESTUDOS E PESQUISAS 2020-IEL-SANDRA/OBSERVATÓRIO/OBSERVATÓRIO FIEG HOME ESPACE/arquivos scripts wendel/caged wendel/extraidos/'
# # arquivo = 'CAGEDMOV202001'
# # df= pd.read_csv(caminho_pasta_extracao+arquivo+'.txt', delimiter=';').astype(np.uint8)

# caminho = caminho_pasta_extracao + "CAGEDMOV202001.txt"
# f=open(caminho)
# lines=f.readlines()
# f.close()
# admissoes_go = 0 
# desligamentos_go = 0
# admissoes_br = 0 
# desligamentos_br = 0

# for line in lines:
     
#     uf = line[9:11]
#     secao = line[19:20]
#     movimentacao = line[29:30]
#     if secao == 'C' and movimentacao == '1':
#         admissoes_br = admissoes_br + 1

#         if uf == '52':
#             admissoes_go = admissoes_go + 1
#     else:
#         if secao == 'C' and movimentacao == '-1':
#             desligamentos_br = desligamentos_br + 1 
#             print('ok')

#             if uf == '52':
#                 desligamentos_go = desligamentos_go + 1 
            
# print(admissoes_br)
# print(desligamentos_br)
# print(admissoes_go)
# print(desligamentos_go)

    







# ########################
# caminho = caminho_pasta_extracao + "CAGEDMOV202001.txt"

# f=open(caminho)
# lines=f.readlines()
# f.close()
# admissoes_go = 0 
# desligamentos_go = 0
# admissoes_br = 0 
# desligamentos_br = 0

# for line in lines:
    
#     uf = line[9:11]
#     secao = line[19:20]
#     movimentacao = line[29:30]
#     if secao == 'C':
#         if movimentacao == '1':
#             admissoes_br = admissoes_br + 1
#         else:
#             desligamentos_br = desligamentos_br + 1 
            
#         if regiao == '52':
#             if movimentacao == '1':
#                 admissoes_go = admissoes_go + 1
#             else:
#                 desligamentos_go = desligamentos_go + 1 
    
    
























# # print(caminho)



# # # with open(caminho_pasta_extracao + "CAGEDMOV202001.txt", 'r') as f:
# # #     f.readline()

# # # print(f.text)

# # f=open(caminho)
# # lines=f.readlines()
# # f.close()
# # # line = '202001;4;42;420540;F;4120400;-1;752305;999;7;27;44;1;1;0;1;31;0;0;0;2110;4;0;1'

# # from csv import reader
# # import pandas as pd
# # # data=lines[1000000:10000000000]
# # # df=pd.DataFrame_csv(list(reader(data)), sep=';')
# # # df.columns = ['competência','região','uf','município','seção','subclasse','saldomovimentação','cbo2002ocupação','categoria','graudeinstrução','idade','horascontratuais','raçacor','sexo','tipoempregador','tipoestabelecimento','tipomovimentação','tipodedeficiência','indtrabintermitente','indtrabparcial','salário','tamestabjan','indicadoraprendiz','fonte']

# # # data = io.StringIO(line)
# # # df = DataFrame(line,columns = ['competência','região','uf','município','seção','subclasse','saldomovimentação','cbo2002ocupação','categoria','graudeinstrução','idade','horascontratuais','raçacor','sexo','tipoempregador','tipoestabelecimento','tipomovimentação','tipodedeficiência','indtrabintermitente','indtrabparcial','salário','tamestabjan','indicadoraprendiz','fonte'])
# # print(lines[2877915])

# # # df= pd.read_csv(lines[1], delimiter=';')


# # caminho = caminho_pasta_extracao + "CAGEDMOV202001.txt"

# # f=open(caminho)
# # lines=f.readlines()
# # f.close()

# # for line in lines:
# #     print(line)

















# # import csv
# # import os    
# # import urllib.parse
# # import requests
# # import numpy as np
# # import json
# # import ftplib
# # import patoolib
# # from bs4 import BeautifulSoup
# # from urllib.request import urlopen
# # import pandas as pd
# # from datetime import date
# # from pyunpack import Archive
# # from sys import getsizeof

# # import io

# # caminho_pasta_extracao = 'G:/IEL/ATENDIMENTO AO CLIENTE WEB 2020/00000 PLANEJAMENTO DESENV EMPRESARIAL 2020/00003 PLANEJAMENTO ESTUDOS E PESQUISAS 2020-IEL-SANDRA/OBSERVATÓRIO/OBSERVATÓRIO FIEG HOME ESPACE/arquivos scripts wendel/caged wendel/extraidos/'
# # # arquivo = 'CAGEDMOV202001'
# # # df= pd.read_csv(caminho_pasta_extracao+arquivo+'.txt', delimiter=';').astype(np.uint8)

# # caminho = caminho_pasta_extracao + "CAGEDMOV202001.txt"
# # print(caminho)



# # # with open(caminho_pasta_extracao + "CAGEDMOV202001.txt", 'r') as f:
# # #     f.readline()

# # # print(f.text)

# # f=open(caminho)
# # lines=f.readlines()
# # line = lines[:10000]
# # f.close()
# # # line = '202001;4;42;420540;F;4120400;-1;752305;999;7;27;44;1;1;0;1;31;0;0;0;2110;4;0;1'


# # # data = io.StringIO(line)
# # df = pd.read_csv(line, sep=";", delimiter='\n',names = ('competência','região','uf','município','seção','subclasse','saldomovimentação','cbo2002ocupação','categoria','graudeinstrução','idade','horascontratuais','raçacor','sexo','tipoempregador','tipoestabelecimento','tipomovimentação','tipodedeficiência','indtrabintermitente','indtrabparcial','salário','tamestabjan','indicadoraprendiz','fonte'))
# # print(df)
# # # df= pd.read_csv(lines[1], delimiter=';')



















# # # from py7zr import unpack_7zarchive
# # # import shutil
# # # caminho = 'C:/Users/wendelsouza.iel/Desktop/panorama-economico/'
# # # shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
# # # shutil.unpack_archive(caminho + 'CAGEDMOV202001.7z', caminho+ '/unzip_path')



# # # def getFile(ftp, path, filename):
# # #     try:
# # #         ftp.retrbinary("RETR " + filename, open(path + filename, 'wb').write)
# # #     except:
# # #         print("Error")

# # # caminho_pasta_compactados = 'G:\IEL\ATENDIMENTO AO CLIENTE WEB 2020/00000 PLANEJAMENTO DESENV EMPRESARIAL 2020/00003 PLANEJAMENTO ESTUDOS E PESQUISAS 2020-IEL-SANDRA/OBSERVATÓRIO/OBSERVATÓRIO FIEG HOME ESPACE/arquivos scripts wendel/caged wendel/compactados/'

# # # #Conectando-se ao endereço
# # # ftp = ftplib.FTP("ftp.mtps.gov.br")
# # # ftp.login()
# # # ftp.encoding = "LATIN-1"
# # # ftp.cwd('pdet/microdados/NOVO CAGED/Movimentações/2020/Outubro')
# # # getFile(ftp, caminho_pasta_compactados, 'CAGEDMOV202010.7z')



# # # meses_ano = ['Dezembro','Novembro','Outubro','Setembro','Agosto','Julho',
# # #          'Junho','Maio','Abril','Março','Fevereiro','Janeiro']

# # # meses_ano1 = ['Outubro','Setembro','Agosto','Julho',
# # #          'Junho','Maio','Abril','Março','Fevereiro','Janeiro']  


# # # for mes in meses_ano:    
# # #     if mes in meses_ano1:
# # #         print(mes)
        
# # #         break

















# # # #Pasta que será navegada
 
# # # # path_dir = os.path.basename('ftp.mtps.gov.br/pdet/microdados/')
# # # ftp.cwd('pdet/microdados/NOVO CAGED/')
# # # files_list = ftp.nlst()
# # # for filename in files_list:
# # #     print(filename) 
# # # # print(ftp.retrlines('LIST') )

# # # path_dir = os.path.commonpath(['pdet/microdados/'])
# # # # ftp.cwd(path_dir)
# # # print(path_dir)