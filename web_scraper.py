
#%% Importando as bibliotecas necessarias:
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import requests
import rows
from io import BytesIO


#%% Link da página dos dados sobre o COVID-19 de Joinville
url_jlle = 'https://www.joinville.sc.gov.br/publicacoes/dados-casos-coronavirus-municipio-de-joinville/'


#%% Tentando acessar a pagina
try:
    html = urlopen(url_jlle)
except HTTPError as e:
    print(e)
    exit()
except URLError as e:
    print(e)
    exit()


#%% Extraindo as tabelas com os dados da pagina
bs = BeautifulSoup(html, 'lxml')
tables = bs.select('.table-responsive')
days = []


#%% Tabela 1: A partir do dia 17/04
table = []
day = {}
count = 0

table = tables[0].find_all('td')

for row in table:
    if count >= 12:
        if row.get_text().find('(') != -1:
            info = row.get_text().split(" ")[0]
        else:
            info = row.get_text()

        if count % 12 == 0:
            date = row.get_text().split(" ")[0].split("/")

            date_iso = date[2] + '-' + date[1] + '-' + date[0]
            day['data_iso'] = date_iso

            day['data'] = row.get_text().split(" ")[0]
            day['hora'] = row.get_text().split(" ")[1]
            
        elif count % 12 == 1:
            day['recuperados'] = int(info)
        elif count % 12 == 2:
            day['internados'] = int(info)
        elif count % 12 == 3:
            day['isolam_domic'] = int(info)
        elif count % 12 == 4:
            day['obitos'] = int(info)
        elif count % 12 == 5:
            day['confirmados'] = int(info)
        elif count % 12 == 6:
            day['intern_uti'] = int(info)
        elif count % 12 == 7:
            day['intern_enferm'] = int(info)
        elif count % 12 == 9:
            day['notificados'] = int(info)
        elif count % 12 == 10:
            day['descartados'] = int(info)
        elif count % 12 == 11:
            day['aguard_exame'] = int(info)
            days.append(day)
            day = {}
    count += 1


#%% Tabela 2: Dados ate o dia 16/04
table = []
day = {}
count = 0

table = tables[1].find_all('td')

for row in table:
    if count % 7 == 0:
        date = row.get_text().split(" ")[0].split("/")

        date_iso = date[2] + '-' + date[1] + '-' + date[0]
        day['data_iso'] = date_iso

        day['data'] = row.get_text().split(" ")[0]
        day['hora'] = row.get_text().split(" ")[1]
    elif count % 7 == 1:
        day['notificados'] = int(row.get_text())
    elif count % 7 == 2:
        day['descartados'] = int(row.get_text())
    elif count % 7 == 3:
        day['aguard_exame'] = int(row.get_text())
    elif count % 7 == 4:
        day['confirmados'] = int(row.get_text())
    elif count % 7 == 5:
        try:
            day['recuperados'] = int(row.get_text())
        except:
            pass
    elif count % 7 == 6:
        day['obitos'] = int(row.get_text())
        days.append(day)
        day = {}
    count += 1


#%% Removendo registros que tenham mais de um registro por dia
aux_days = []

for count in range(len(days)):
    if count == 0:
        aux_days.append(days[count])
    elif days[count]['data'] != days[count-1]['data']:
        aux_days.append(days[count])

days = aux_days


#%% Gerando um dataframe com os dados do Brasil.IO: Covid-19 e de Joinville
rows_dados = rows.import_from_dicts(days)

url_brasil_io = 'https://brasil.io/dataset/covid19/caso_full/?format=csv'

csv_brasil = requests.get(url_brasil_io).content

rows_brasil = rows.import_from_csv(BytesIO(csv_brasil))


#%% Gerando informacoes relativas a populacao de Joinville
pop_jlle = [row.estimated_population_2019 for row in rows_brasil if row.city == 'Joinville']
pop_jlle = pop_jlle[0]

conf_100k = []
taxa_obito = []
obito_100k = []

for i in range(len(rows_dados)):
    
    conf_atual = rows_dados[i].confirmados
    obito_atual = rows_dados[i].obitos

    conf_100k.append(round(((conf_atual * 100000) / pop_jlle), 3))
    taxa_obito.append(round((obito_atual / conf_atual), 3))
    obito_100k.append(round(((obito_atual * 100000) / pop_jlle), 3))


#%% Adicionando as informacoes para o dataframe principal
rows_dados['conf_por_100k'] = conf_100k

rows_dados['taxa_conf_obito'] = taxa_obito

rows_dados['obito_por_100k'] = obito_100k


#%% Exportando os dados das cidades brasileiras para .CSV e .XLSX
rows.export_to_csv(rows_brasil, "covid_brasil.csv") 

rows.export_to_xlsx(rows_brasil, "covid_brasil.xlsx")


#%% Criando rows.Table e exportando para .CSV e .XLSX
rows.export_to_csv(rows_dados, "covid_joinville.csv")

rows.export_to_xlsx(rows_dados, "covid_joinville.xlsx")
