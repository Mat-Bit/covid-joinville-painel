
#%% Importando as bibliotecas necessarias:
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import rows


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
            hour = row.get_text().split(" ")[1].split(":")

            date_hour = date[2] + date[1] + date[0] + hour[0] + hour[1]
            day['data_hora'] = date_hour

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
        hour = row.get_text().split(" ")[1].split(":")

        date_hour = date[2] + date[1] + date[0] + hour[0] + hour[1]
        day['data_hora'] = date_hour

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


#%% Criando rows.Table e exportando para .CSV e .XLSX
rows_table = rows.import_from_dicts(days)

rows.export_to_csv(rows_table, "covid_joinville.csv")

rows.export_to_xlsx(rows_table, "covid_joinville.xlsx")
