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
