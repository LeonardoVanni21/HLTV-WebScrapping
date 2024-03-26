# HLTV-WebScrapping

## Descrição

Esse é um projeto de web scrapping que raspa o site da HLTV para os últimos torneios de CS2 e seus detalhes, e também o ranking de players de toda a história do CS com pelo menos 50 mapas jogados entre times top 30 da HLTV. O projeto é escrito em Python e usa a biblioteca BeautifulSoup para raspar o site.
Foi feito para a disciplina de Desenvolvimento de Sistemas Distribuídos da Unisenai de Chapecó/SC.

## Instalação

Para instalar as dependências do projeto, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Uso

Para rodar o projeto, apenas execute o arquivo `main.py`, e informe o que deseja acessar rank ou torneio e em caso de torneio informe a url do mesmo.

```bash
python main.py
```

Espere o programa terminar de rodar e verifique o arquivo `data.csv` para ver os resultados.

## Feito por

- [Leonardo Vanni Bonavigo]