from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import conexao

def extrair_classificacao(url):
    options = Options()
    #options.add_argument('--headless')
    navegador = webdriver.Chrome(options=options)
    navegador.get(url)

    sleep(0.5)
    #######################################################################################################################
                                ## Busca dos elementos da página ##
    #######################################################################################################################

    tabela = navegador.find_element_by_tag_name('article') #Elemento article encontrado através do inpsecionar do chrome
    htmlTabela = tabela.get_attribute("outerHTML") #codigo html do article
    soup = BeautifulSoup(htmlTabela,'html.parser') #transforma o html em objeto do beautiful soup
    #O codigo da pagina divide a tabela em uma tabela de equipes e uma de pontos
    #Busca tabela de equipes
    tabelaEquipe = soup.find('table',{'class':'tabela__equipes tabela__equipes--com-borda'})
    #Busca tabela de pontos
    tabelaPontos = soup.find('table',{'class':'tabela__pontos'})

    # Buscar número da rodada

    tagRodada = navegador.find_element_by_class_name("lista-jogos__navegacao--rodada")
    htmlRodada = tagRodada.get_attribute("outerHTML")
    rodadaSoup = BeautifulSoup(htmlRodada, 'html.parser')

    rodadaText = rodadaSoup.text
    rodadaAux = ""

    for i in rodadaText:
        if i.isdigit():
            rodadaAux += i

    rodadaNum = int(rodadaAux)

    #######################################################################################################################
                                ## Tratamentos dos dados trazidos pelo HTML ##
    #######################################################################################################################

    #Da tabela de equipes, buscamos a posição do time na tabela (classificação)
    classificacoes = tabelaEquipe.findAll('td', attrs={'class': 'classificacao__equipes classificacao__equipes--posicao'})

    #Busca o nome da equipe
    times = tabelaEquipe.findAll('td', attrs={'class': 'classificacao__equipes classificacao__equipes--time'})
    #Na tabela de pontos, os valores de todas as colunas vem em uma unica linha

    #Buscamos a linha com os valores
    linhaPontos = tabelaPontos.findAll('tr', attrs={'class':'classificacao__tabela--linha'})

    #criamos uma lista para guardar os valores de cada célula
    valores =[]
    listaClassificacao =[]

    for linha in linhaPontos:
        # Encontre todas as células 'td' na linha
        celulas = linha.find_all('td')

        # Extraia o texto de cada célula e adicione-o à lista 'valores'
        valores_linha = [celula.text.strip() for celula in celulas]

        # Converta a lista de valores da linha em uma string separada por vírgulas
        linha_como_string = ','.join(valores_linha).rstrip(',')

        # Adicione a string resultante à lista 'valores'
        valores.append(linha_como_string)

    # Agora, 'valores' conterá os valores separados por vírgulas de cada linha


    listaClassificacao =[] #lista de dicionários
    for classificacao, time,valor in zip(classificacoes,times,valores):

        classificacao_info = { #Dicionario com as informações de cada time
            'Classificacao': int(classificacao.text),
            'Time': time.find('strong').text, # O nome dos times se encontram na tag strong
            'Valores': valor
        }
        listaClassificacao.append(classificacao_info)


    df = pd.DataFrame(listaClassificacao) #Transforma a lista em um dataframe

    # Salva os dados na tabela tb_classificacao no sql server
    cursor = conexao.conn.cursor()

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO tb_classificacao (classificacao, equipe, valores,num_rodada) VALUES (?, ?, ?,?)",
                       row.Classificacao, row.Time, row.Valores, rodadaNum)
    conexao.conn.commit()
    cursor.close()
    navegador.quit()













