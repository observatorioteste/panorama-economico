set /A COUNTER=1
chcp 65001
@ECHO OFF
:loop
echo %Counter%
cls
echo ATUALIZANDO 'Utilização da Capacidade Instalada da Indústria' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\capacidade_industria_transf.py"
echo 'Utilização da Capacidade Instalada da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Exportações e importações' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\comex.py"
echo 'Exportações e importações' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice de Confiança Industrial' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\confianca_industrial.py"
echo 'Índice de Confiança Industrial' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Taxa de Desocupação' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\desocupacao.py"
echo 'Taxa de Desocupação' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Estoque efetivo em relação ao planejado da Indústria' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\estoque_efetivo.py"
echo 'Estoque efetivo em relação ao planejado da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls


echo %Counter%
cls
echo ATUALIZANDO 'Perspectiva do Emprego da Indústria' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\expectativa_emprego.py"
echo 'Perspectiva do Emprego da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice de Atividade Econômica' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\ibc.py"
echo 'Índice de Atividade Econômica' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice de Confiança do Consumidor' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\icc_novo.py"
echo 'Índice de Confiança do Consumidor' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice Geral de Preços – Mercado (IGP-M)' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\igpm.py"
echo 'Índice Geral de Preços – Mercado (IGP-M)' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice Nacional de Preços ao Consumidor - INPC' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\inpc.py"
echo 'Índice Nacional de Preços ao Consumidor - INPC' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Intenção de Investir na Indústria' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\intencao_invest.py"
echo 'Intenção de Investir na Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice Nacional de Preços ao Consumidor Amplo - IPCA' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\ipca.py"
echo 'Índice Nacional de Preços ao Consumidor Amplo - IPCA' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Produção Física Industrial' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\pim.py"
echo 'Produção Física Industrial' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Saldo de Empregados da Ind. de Transformação' [%Counter%/14]
{user}AppData/Local/Microsoft/WindowsApps/python.exe "{path}scripts\saldo_desemprego_caged.py"
echo 'Saldo de Empregados da Ind. de Transformação' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

cls
echo A execução será retomada em alguns minutos...
timeout /t 3600 /nobreak > nul

set /A COUNTER=1

goto loop