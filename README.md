# Painel COVID-19 Joinville

Painel dos casos de COVID-19 em Joinville/SC e script para obter os dados estruturados.

**Fonte:** [Site Prefeitura de Joinville](https://www.joinville.sc.gov.br/publicacoes/dados-casos-coronavirus-municipio-de-joinville/)


- [Visualizar o Painel Interativo](#Visualizar_o_Painel_Interativo)
- [Obter arquivo CSV](#Obter_arquivo_CSV)
- [Baixar e executar o script que gera o arquivo CSV](#Baixar_e_executar_o_script_que_gera_o_arquivo_CSV)


## Visualizar o Painel Interativo

Para visualizar um painel interativo sobre os casos de COVID-19 clique no link abaixo: 
**[Acessar o Painel](https://datastudio.google.com/s/rxtWEbmtvec)**


## Obter arquivo CSV

Para obter o arquivo CSV dos dados atualizados diariamente **[clique aqui](https://drive.google.com/open?id=1Ok3982frtseLW8izQpfvl6ZkzLtj4bpN)**


## Baixar e executar o script que gera o arquivo CSV

### Dependências

- Python >= 3.6

O script é um arquivo Python, caso ainda não tenha instalado em sua máquina, [baixe aqui](https://www.python.org/downloads/).

### Instalando as bibliotecas e executando o script

Neste sricpt foi utilizado uma biblioteca open-source brasileira muito bacana:

**[rows](https://github.com/turicas/rows)** 

(Obrigado [Turicas](https://github.com/turicas) !)

#### Passos

1. Utilizando um terminal, vá para a pasta que deseja copiar o projeto:

```shell
cd minha/pasta/ 
```

2. Copie este projeto para seu repositório local:

```shell
git clone https://github.com/Mat-Bit/covid-joinville-painel.git
```

3. Acesse seu repositório local:

```shell
cd covid-joinville-painel/
```

4. Com o interpretador Python configurado, execute a instalação das bibliotecas:

```shell
pip install -r requirements.txt
```

6. Por fim, execute o script:

```shell
python web_scraper.py
```


## Executando o script com o Jupyter Notebook

Outra opção mais prática para executar o script sem a necessidade de ter o Python instalado em sua máquina, é utilizando o **Jupyter Notebook**.

Para isto, basta selecionar o arquivo `web_scraper.ipynb` e fazer o upload para o **Google Drive**, clique com o botão direito no mouse no arquivo e selecione a opção **abrir com** e escolha o aplicativo *Google Collaboratory*.