import pandas as pd
import numpy as np

partidas = pd.read_csv("campeonato-brasileiro-full.csv")
estatisticas = pd.read_csv("campeonato-brasileiro-estatisticas-full.csv")
gols = pd.read_csv("campeonato-brasileiro-gols.csv")
cartoes = pd.read_csv("campeonato-brasileiro-cartoes.csv")

partidas["data"] = pd.to_datetime(
    partidas["data"],
    format="%d/%m/%Y"
)

partidas["ano"] = partidas["data"].dt.year
partidas["mes"] = partidas["data"].dt.month
partidas["dia"] = partidas["data"].dt.day
partidas["dia_semana"] = partidas["data"].dt.day_name()

partidas["gols_partida"] = (
    partidas["mandante_Placar"] +
    partidas["visitante_Placar"]
)

partidas["Resultado"] = np.where(
    partidas["mandante_Placar"] > partidas["visitante_Placar"], "Vitoria Mandante",
    np.where(
        partidas["mandante_Placar"] < partidas["visitante_Placar"], "Vitoria Visitante", "Empate"
    )
)

partidas["Saldo_mandante"] = (
    partidas["mandante_Placar"] - partidas["visitante_Placar"]
)

clubes_mandante = partidas[["mandante", "mandante_Estado"]].copy()

clubes_mandante.columns = ["clube", "estado"]

clubes_visitante = partidas[["visitante", "visitante_Estado"]].copy()

clubes_visitante.columns = ["clube", "estado"]

dim_clube = pd.concat([clubes_mandante, clubes_visitante], axis=0)

dim_clube = dim_clube.drop_duplicates("clube").reset_index(drop=True)

dim_clube["id_clube"] = dim_clube.index + 1

dim_clube["clube"].value_counts()
sorted(dim_clube["clube"].unique())

stats = estatisticas.merge(
    partidas[["ID", "ano", "data", "mandante", "visitante", "vencedor", "resultado"]],
    left_on="partida_id",
    right_on="ID",
    how="left"
)

stats["local"] = np.where(
    stats["clube"] == stats["mandante"],
    "Mandante",
    "Visitante"
)

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
