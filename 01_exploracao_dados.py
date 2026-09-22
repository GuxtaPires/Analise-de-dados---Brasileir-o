import pandas as pd
import numpy as np
import os

# ============================================================
# 2. LEITURA DOS ARQUIVOS CSV
# ============================================================

# Carrega o arquivo com as informações gerais das partidas.
# Cada linha representa uma partida.
partidas = pd.read_csv("campeonato-brasileiro-full.csv")

# Carrega o arquivo com as estatísticas das equipes em cada partida.
# Cada partida possui registros para as duas equipes.
estatisticas = pd.read_csv("campeonato-brasileiro-estatisticas-full.csv")

# Carrega o arquivo com os eventos de gols.
# Cada linha representa um gol.
gols = pd.read_csv("campeonato-brasileiro-gols.csv")

# Carrega o arquivo com os eventos de cartões.
# Cada linha representa um cartão.
cartoes = pd.read_csv("campeonato-brasileiro-cartoes.csv")


# ============================================================
# 3. TRATAMENTO DA DATA
# ============================================================

# Converte a coluna "data", que inicialmente está como texto,
# para o formato de data reconhecido pelo Pandas.
#
# O parâmetro format="%d/%m/%Y" informa que a data está no formato:
# dia/mês/ano
#
# Exemplo:
# "29/03/2003" -> 2003-03-29
partidas["data"] = pd.to_datetime(
    partidas["data"],
    format="%d/%m/%Y"
)


# ============================================================
# 4. CRIAÇÃO DE VARIÁVEIS RELACIONADAS À DATA
# ============================================================

# Extrai o ano da data da partida.
# Exemplo: 29/03/2003 -> 2003
partidas["ano"] = partidas["data"].dt.year

# Extrai o mês da data.
# Exemplo: 29/03/2003 -> 3
partidas["mes"] = partidas["data"].dt.month

# Extrai o dia do mês.
# Exemplo: 29/03/2003 -> 29
partidas["dia"] = partidas["data"].dt.day

# Identifica o dia da semana.
# Exemplo: uma determinada data pode retornar "Saturday".
partidas["dia_semana"] = partidas["data"].dt.day_name()


# ============================================================
# 5. CRIAÇÃO DO TOTAL DE GOLS DA PARTIDA
# ============================================================

# Soma os gols marcados pelo mandante e pelo visitante.
#
# Exemplo:
# Mandante = 3
# Visitante = 1
# gols_partida = 4
partidas["gols_partida"] = (
    partidas["mandante_Placar"] +
    partidas["visitante_Placar"]
)


# ============================================================
# 6. CRIAÇÃO DO RESULTADO DA PARTIDA
# ============================================================

# Cria uma nova coluna chamada "Resultado".
#
# np.where funciona como um "SE" / "IF":
#
# Se a condição for verdadeira -> primeiro resultado
# Se for falsa -> segundo resultado
#
# Aqui temos três possibilidades:
#
# Mandante fez mais gols:
#     "Vitoria Mandante"
#
# Visitante fez mais gols:
#     "Vitoria Visitante"
#
# Caso nenhuma das duas condições seja verdadeira:
#     "Empate"
partidas["Resultado"] = np.where(
    partidas["mandante_Placar"] > partidas["visitante_Placar"],
    "Vitoria Mandante",
    np.where(
        partidas["mandante_Placar"] < partidas["visitante_Placar"],
        "Vitoria Visitante",
        "Empate"
    )
)


# ============================================================
# 7. CRIAÇÃO DO SALDO DE GOLS DO MANDANTE
# ============================================================

# Calcula a diferença entre os gols do mandante e os gols
# do visitante.
#
# Exemplo:
# Mandante = 3
# Visitante = 1
# Saldo = 2
#
# Se o resultado for negativo, significa que o mandante
# perdeu por aquela diferença.
partidas["Saldo_mandante"] = (
    partidas["mandante_Placar"] -
    partidas["visitante_Placar"]
)


# ============================================================
# 8. INÍCIO DA CRIAÇÃO DA DIMENSÃO DE CLUBES
# ============================================================

# Seleciona apenas as colunas relacionadas ao clube mandante
# e ao seu estado.
#
# O .copy() cria uma cópia independente desse DataFrame.
clubes_mandante = partidas[
    ["mandante", "mandante_Estado"]
].copy()


# Renomeia as colunas para uma estrutura genérica.
#
# Antes:
# mandante | mandante_Estado
#
# Depois:
# clube | estado
clubes_mandante.columns = [
    "clube",
    "estado"
]


# Fazemos a mesma coisa para os clubes visitantes.
clubes_visitante = partidas[
    ["visitante", "visitante_Estado"]
].copy()


# Renomeia as colunas dos visitantes para o mesmo padrão
# utilizado nos mandantes.
clubes_visitante.columns = [
    "clube",
    "estado"
]


# ============================================================
# 9. COMBINAÇÃO DOS CLUBES
# ============================================================

# Junta verticalmente os clubes mandantes e visitantes.
#
# axis=0 significa que estamos adicionando linhas.
#
# Exemplo:
#
# Mandantes:
# Guarani
# Vasco
# Santos
#
# Visitantes:
# Corinthians
# Flamengo
# Palmeiras
#
# Resultado:
# Guarani
# Vasco
# Santos
# Corinthians
# Flamengo
# Palmeiras
dim_clube = pd.concat(
    [clubes_mandante, clubes_visitante],
    axis=0
)


# Remove clubes duplicados.
#
# Estamos considerando somente a coluna "clube".
#
# Assim, se "Santos" aparecer centenas de vezes,
# ficará apenas uma ocorrência.
#
# reset_index(drop=True) reorganiza o índice depois da remoção
# das duplicatas.
dim_clube = dim_clube.drop_duplicates(
    "clube"
).reset_index(drop=True)


# ============================================================
# 10. CRIAÇÃO DO ID DO CLUBE
# ============================================================

# Cria um identificador numérico para cada clube.
#
# O índice começa em 0, então adicionamos 1 para que os IDs
# comecem em 1.
#
# Exemplo:
#
# índice 0 -> id_clube 1
# índice 1 -> id_clube 2
# índice 2 -> id_clube 3
dim_clube["id_clube"] = dim_clube.index + 1


# ============================================================
# 11. VERIFICAÇÃO DOS CLUBES
# ============================================================

# Conta quantas vezes cada clube aparece.
#
# Como já removemos as duplicatas, cada clube deverá aparecer
# apenas uma vez.
dim_clube["clube"].value_counts()


# Cria uma lista ordenada alfabeticamente com os clubes únicos.
#
# É uma forma simples de conferir se existem nomes diferentes
# que poderiam representar o mesmo clube.
sorted(
    dim_clube["clube"].unique()
)


# ============================================================
# 12. CRIAÇÃO DA TABELA DE ESTATÍSTICAS
# ============================================================

# Faz um MERGE entre a tabela de estatísticas e informações
# da tabela de partidas.
#
# Queremos adicionar às estatísticas:
# - ID da partida
# - ano
# - data
# - mandante
# - visitante
# - vencedor
# - resultado
#
# left_on="partida_id":
# coluna usada na tabela estatisticas.
#
# right_on="ID":
# coluna correspondente na tabela partidas.
#
# how="left":
# mantém todas as linhas existentes em estatisticas.
stats = estatisticas.merge(
    partidas[
        [
            "ID",
            "ano",
            "data",
            "mandante",
            "visitante",
            "vencedor",
            "resultado"
        ]
    ],
    left_on="partida_id",
    right_on="ID",
    how="left"
)


# ============================================================
# 13. IDENTIFICAÇÃO DE MANDANTE E VISITANTE
# ============================================================

# np.where verifica se o clube daquela linha de estatísticas
# é o mesmo clube que aparece como mandante.
#
# Se for:
#     "Mandante"
#
# Caso contrário:
#     "Visitante"
stats["local"] = np.where(
    stats["clube"] == stats["mandante"],
    "Mandante",
    "Visitante"
)


# ============================================================
# 14. RESULTADO DO CLUBE
# ============================================================

# Cria uma classificação do resultado olhando para o clube
# daquela linha.
#
# Existem três possibilidades:
#
# 1. Vencedor = "-"
#    -> Empate
#
# 2. O clube da linha é o vencedor
#    -> Vitória
#
# 3. Qualquer outra situação
#    -> Derrota
stats["resultado_clube"] = np.select(
    [
        stats["vencedor"] == "-",
        stats["clube"] == stats["vencedor"]
    ],
    [
        "Empate",
        "Vitória"
    ],
    default="Derrota"
)


# ============================================================
# 15. CRIAÇÃO DA TABELA DE GOLS
# ============================================================

# Faz o merge da tabela de gols com informações das partidas.
#
# Assim conseguimos saber, além do gol:
# - ano da partida
# - data
# - mandante
# - visitante
# - resultado
#
# A granularidade continua sendo:
# 1 linha = 1 gol.
fato_gols = gols.merge(
    partidas[
        [
            "ID",
            "ano",
            "data",
            "mandante",
            "visitante",
            "resultado"
        ]
    ],
    left_on="partida_id",
    right_on="ID",
    how="left"
)


# ============================================================
# 16. CRIAÇÃO DA TABELA DE CARTÕES
# ============================================================

# Faz o mesmo processo realizado com os gols,
# agora para os cartões.
#
# A granularidade continua sendo:
# 1 linha = 1 cartão.
fato_cartoes = cartoes.merge(
    partidas[
        [
            "ID",
            "ano",
            "data",
            "mandante",
            "visitante",
            "resultado"
        ]
    ],
    left_on="partida_id",
    right_on="ID",
    how="left"
)


# ============================================================
# 17. CRIAÇÃO DO DIRETÓRIO PARA OS DADOS TRATADOS
# ============================================================

# Cria a pasta:
#
# data/
# └── processed/
#
# exist_ok=True significa que, caso a pasta já exista,
# o Python não apresentará erro.
os.makedirs(
    "data/processed",
    exist_ok=True
)


# ============================================================
# 18. SALVAMENTO DAS BASES TRATADAS
# ============================================================

# Salva a tabela de partidas tratada.
#
# index=False evita que o índice do DataFrame seja salvo
# como uma coluna adicional no CSV.
partidas.to_csv(
    "data/processed/partidas.csv",
    index=False
)


# Salva a dimensão de clubes.
dim_clube.to_csv(
    "data/processed/dim_clube.csv",
    index=False
)


# Salva a tabela de estatísticas.
stats.to_csv(
    "data/processed/stats.csv",
    index=False
)


# Salva a tabela de gols.
fato_gols.to_csv(
    "data/processed/fato_gols.csv",
    index=False
)


# Salva a tabela de cartões.
fato_cartoes.to_csv(
    "data/processed/fato_cartoes.csv",
    index=False
)
