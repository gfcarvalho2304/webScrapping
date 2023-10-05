import requests
from bs4 import BeautifulSoup
import pandas as pd
import conexao

def extrair_artilharia(url):

    response = requests.get(url)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    colocacoes = site.findAll('div', attrs={'class': 'ranking-item'})
    jogadores = site.findAll('div', attrs={'class': 'jogador-nome'})
    posicoes = site.findAll('div', attrs={'class': 'jogador-posicao'})
    gols = site.findAll('div', attrs={'class': 'jogador-gols'})
    fotos_jogadores = site.findAll('div', attrs={'class': 'jogador-foto'})
    escudos_jogadores = site.findAll('div', attrs={'class': 'jogador-escudo'})

    info_jogadores = []
    colocacao_anterior = 0

    for colocacao, jogador, posicao, gol, foto_jogador, escudo_jogador in zip(colocacoes, jogadores, posicoes, gols, fotos_jogadores, escudos_jogadores):
        if colocacao.text.strip():
            colocacao_anterior = int(colocacao.text)

        foto_jogador_element = foto_jogador.find('img')  # Encontre o elemento <img> dentro de <div class="jogador-foto">
        foto_jogador_url = foto_jogador_element['src'] if foto_jogador_element else ''  # Obtenha o atributo 'src' da imagem ou defina como vazio

        escudo_jogador_element = escudo_jogador.find('img')  # Encontre o elemento <img> dentro de <div class="jogador-escudo">
        escudo_jogador_url = escudo_jogador_element['src'] if escudo_jogador_element else ''  # Obtenha o atributo 'src' do escudo ou defina como vazio
        clube_jogador = escudo_jogador_element['alt'] if escudo_jogador_element else '' #pega o nome do clube

        jogador_info = {
            'Colocacao': colocacao_anterior,
            'Jogador': jogador.text,
            'Posicao': posicao.text,
            'Gols': int(gol.text),
            'Foto_jogador': foto_jogador_url,
            'Escudo_jogador': escudo_jogador_url,
            'Clube': clube_jogador
        }

        info_jogadores.append(jogador_info)

    df = pd.DataFrame(info_jogadores)

    cursor = conexao.conn.cursor()

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO tb_artilharia (ranking, nome_jogador, posicao, gols, jogador_foto, jogador_escudo,clube) VALUES (?, ?, ?, ?, ?, ?,?)",
                       row.Colocacao, row.Jogador, row.Posicao, row.Gols, row.Foto_jogador, row.Escudo_jogador,row.Clube)
    conexao.conn.commit()
    cursor.close()
