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
pop_jlle = 590466.0

table = tables[1].find_all('td')

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

            day['conf_por_100k'] = round(((day['confirmados'] * 100000) / pop_jlle), 3)

            day['taxa_conf_obito'] = round((day['obitos'] / day['confirmados']), 3)

            day['obito_por_100k'] = round(((day['obitos'] * 100000) / pop_jlle), 3)

            days.append(day)
            day = {}
    count += 1


#%% Tabela 4: Dados ate o dia 16/04
table = []
day = {}
count = 0

table = tables[4].find_all('td')

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

        day['conf_por_100k'] = round(((day['confirmados'] * 100000) / pop_jlle), 3)
        day['taxa_conf_obito'] = round((day['obitos'] / day['confirmados']), 3)
        day['obito_por_100k'] = round(((day['obitos'] * 100000) / pop_jlle), 3)

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

rows_dados = rows.import_from_dicts(days)


#%% Tabela 2: Ocupacao leitos UTI para COVID-19
days = []
table = []
day = {}
count = 0

table = tables[2].find_all('td')

for row in table:
    if row.get_text().find('(') != -1:
        info = row.get_text().split(" ")[0]
    else:
        info = row.get_text()

    if count % 6 == 0:
        date = row.get_text().split(" ")[0].split("/")

        date_iso = date[2] + '-' + date[1] + '-' + date[0]
        day['data_iso'] = date_iso

        day['data'] = row.get_text().split(" ")[0]
        day['hora'] = row.get_text().split(" ")[1]
    elif count % 6 == 1:
        day['uti_confirmados'] = int(info)
    elif count % 6 == 2:
        day['uti_descartados'] = int(info)
    elif count % 6 == 3:
        day['uti_aguard_result'] = int(info)
    elif count % 6 == 4:
        day['uti_disponivel'] = int(info)
    elif count % 6 == 5:
        day['uti_total'] = int(info)

        days.append(day)
        day = {}

    count += 1


#%% Tabela 3: Ocupacao leitos de Enfermaria para COVID-19
table = []
day = {}
count = 0

table = tables[3].find_all('td')

for row in table:
    if row.get_text().find('(') != -1:
        info = row.get_text().split(" ")[0]
    else:
        info = row.get_text()

    if count % 6 == 0:
        date = row.get_text().split(" ")[0].split("/")

        date_iso = date[2] + '-' + date[1] + '-' + date[0]
        day['data_iso'] = date_iso

        day['data'] = row.get_text().split(" ")[0]
        day['hora'] = row.get_text().split(" ")[1]
    elif count % 6 == 1:
        day['enf_confirmados'] = int(info)
    elif count % 6 == 2:
        day['enf_descartados'] = int(info)
    elif count % 6 == 3:
        day['enf_aguard_result'] = int(info)
    elif count % 6 == 4:
        day['enf_disponivel'] = int(info)
    elif count % 6 == 5:
        day['enf_total'] = int(info)

        for d in days:
            if d['data_iso'] == day['data_iso']:
                d.update(day)
        day = {}

    count += 1

rows_leitos = rows.import_from_dicts(days)


#%% Armazenando em uma lista de dicionarios os dados do Brasil.IO: Covid-19
days_brasil = []

url_brasil_io = 'https://brasil.io/api/dataset/covid19/caso_full/data/'
resp = requests.get(url_brasil_io)
json_resp = resp.json()

while json_resp['next'] != 'null':
    for r in json_resp['results']:
        days_brasil.append(r)

    if json_resp['next'] is None:
        break

    url_brasil_io = json_resp['next']
    resp = requests.get(url_brasil_io)
    json_resp = resp.json()


#%% Atualizando nesta lista o ultimo registro da cidade de Joinville

for day in days_brasil:
    if day['city'] == 'Joinville' and day['is_last'] == True:
        day['date'] = rows_dados[0].data_iso
        day['last_available_confirmed'] = rows_dados[0].confirmados
        day['last_available_confirmed_per_100k_inhabitants'] = rows_dados[0].conf_por_100k
        day['new_confirmed'] = rows_dados[0].confirmados - rows_dados[1].confirmados
        day['last_available_deaths'] = rows_dados[0].obitos
        day['new_deaths'] = rows_dados[0].obitos - rows_dados[1].obitos
        day['last_available_death_rate'] = rows_dados[0].taxa_conf_obito
        break

rows_brasil = rows.import_from_dicts(days_brasil)


#%% Exportando os dados das cidades brasileiras para .CSV e .XLSX
rows.export_to_csv(rows_brasil, "covid_brasil.csv")

rows.export_to_xlsx(rows_brasil, "covid_brasil.xlsx")


#%% Exportando os dados sobre joinville para .CSV e .XLSX
rows.export_to_csv(rows_dados, "covid_joinville.csv")

rows.export_to_xlsx(rows_dados, "covid_joinville.xlsx")


#%% Exportando os dados sobre ocupacao dos leitos para .CSV e .XLSX
rows.export_to_csv(rows_leitos, "leitos_uti_enfermaria.csv")

rows.export_to_xlsx(rows_leitos, "leitos_uti_enfermaria.xlsx")
