from classificacao import extrair_classificacao
from artilharia import extrair_artilharia
import conexao
from functions import retorna_rodada,enviar_email

#Busca o número da rodada atual
num_rodada = retorna_rodada('https://ge.globo.com/futebol/brasileirao-serie-a/')

#Busca Número da última rodada salva
cursor = conexao.conn.cursor()
cursor.execute("select max(num_rodada) from tb_classificacao")
rodada_anterior = cursor.fetchone()[0]

#Executa a carga se o número da rodada atual for maior que o da última salva
if num_rodada > rodada_anterior:

    extrair_classificacao('https://ge.globo.com/futebol/brasileirao-serie-a/')
    extrair_artilharia('https://ge.globo.com/futebol/brasileirao-serie-a/')
#Como na carga da tabela artilharia não buscamos o número da rodada, atualizamos com o número da rodada trazido na carga da tabela de classificação
    cursor.execute("update tb_artilharia set num_rodada =(select max(num_rodada) from tb_classificacao) where num_rodada is null")
    conexao.conn.commit()
    cursor.close()
    enviar_email('Carga de dados do Brasileirão', f'Tabelas atualizadas com os dados da rodada {num_rodada}')



