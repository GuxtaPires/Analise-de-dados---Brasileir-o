# ⚽ Brasileirão Analytics

## 📊 Uma análise orientada a dados do Campeonato Brasileiro

Projeto de **Data Analytics** desenvolvido com o objetivo de explorar dados históricos do Campeonato Brasileiro, transformando dados brutos de partidas, estatísticas, gols e cartões em análises e visualizações capazes de responder perguntas sobre **desempenho dos clubes, resultados, características das partidas e comportamento dos indicadores ao longo das temporadas**.

O projeto foi desenvolvido com foco em um fluxo completo de análise de dados, passando por **ETL, tratamento e exploração dos dados, modelagem, análise estatística, criação de indicadores e visualização em Power BI**.

---

## 🎯 Objetivos

O principal objetivo é utilizar dados históricos do Campeonato Brasileiro para investigar padrões relacionados ao desempenho das equipes e às características das partidas.

Entre as principais perguntas exploradas estão:

* Como o desempenho dos clubes varia ao longo das temporadas?
* Qual é a distribuição de vitórias, empates e derrotas?
* Existe vantagem em jogar como mandante?
* Como a quantidade de gols varia ao longo dos anos?
* Quais clubes apresentam maior volume ofensivo?
* Qual a relação entre finalizações e gols?
* Como posse de bola, passes, escanteios e outras estatísticas se relacionam com os resultados?
* Em quais períodos das partidas ocorrem mais gols e cartões?
* Como os indicadores de desempenho dos clubes se comportam ao longo do tempo?

> **Importante:** o projeto busca identificar associações e padrões nos dados. Relações observadas entre estatísticas e resultados não são interpretadas automaticamente como relações de causalidade.

---

# 🗂️ Dados

O projeto utiliza quatro conjuntos de dados principais:

### 🏟️ Partidas

Contém informações gerais de cada partida:

* ID da partida
* Rodada
* Data
* Horário
* Mandante
* Visitante
* Formação das equipes
* Técnicos
* Vencedor
* Arena
* Placar
* Estado dos clubes
* Arrecadação

### 📈 Estatísticas das partidas

Contém estatísticas individuais de cada equipe em cada partida:

* Chutes
* Chutes no alvo
* Posse de bola
* Passes
* Precisão de passes
* Faltas
* Cartões amarelos
* Cartões vermelhos
* Impedimentos
* Escanteios

Cada partida possui registros para as duas equipes.

### ⚽ Gols

Contém os eventos de gol registrados nas partidas:

* ID da partida
* Rodada
* Clube
* Atleta
* Minuto
* Tipo de gol

### 🟨 Cartões

Contém os eventos de cartões:

* ID da partida
* Rodada
* Clube
* Tipo de cartão
* Atleta
* Número da camisa
* Posição
* Minuto

---

# 🏗️ Arquitetura do projeto

O projeto segue uma estrutura separando os dados brutos, processamento, análises e visualizações.

```text
brasileirao-data-analytics/
│
├── data/
│   ├── raw/
│   │   ├── campeonato-brasileiro-full.csv
│   │   ├── campeonato-brasileiro-estatisticas-full.csv
│   │   ├── campeonato-brasileiro-gols.csv
│   │   └── campeonato-brasileiro-cartoes.csv
│   │
│   └── processed/
│
├── python/
│   ├── data_cleaning.ipynb
│   └── exploratory_analysis.ipynb
│
├── powerbi/
│   └── brasileirao-analytics.pbix
│
├── images/
│   └── dashboard/
│
└── README.md
```

---

# 🔄 Pipeline de dados

O fluxo de desenvolvimento do projeto segue as seguintes etapas:

```text
Dados brutos
     ↓
Exploração inicial
     ↓
Tratamento e limpeza
     ↓
Criação de variáveis
     ↓
Modelagem dos dados
     ↓
Análise exploratória
     ↓
Criação de indicadores
     ↓
Power BI
     ↓
Dashboard
     ↓
Insights
```

---

# 🐍 Tratamento e análise com Python

O Python é utilizado para exploração, transformação e preparação dos dados.

Principais atividades:

* Leitura dos arquivos CSV
* Inspeção das estruturas
* Identificação dos tipos de dados
* Tratamento de datas
* Criação de variáveis derivadas
* Identificação de valores inconsistentes
* Análise de valores ausentes
* Criação de tabelas dimensionais
* Integração entre partidas e estatísticas
* Análise exploratória

### Principais bibliotecas

```text
Python
Pandas
NumPy
Matplotlib
```

---

# 🧱 Modelagem dos dados

Um dos objetivos do projeto é evitar simplesmente juntar todas as tabelas em uma única estrutura.

As tabelas possuem diferentes níveis de granularidade:

```text
PARTIDAS
1 linha = 1 partida

ESTATÍSTICAS
1 linha = 1 clube em 1 partida

GOLS
1 linha = 1 gol

CARTÕES
1 linha = 1 cartão
```

Essa diferença de granularidade é considerada durante a modelagem para evitar **duplicação de informações e distorção dos indicadores**.

A modelagem busca aproximar o projeto de uma estrutura dimensional, separando informações de partidas, clubes e eventos.

---

# 📐 Variáveis derivadas

Durante o tratamento dos dados são criadas novas variáveis para facilitar as análises.

Entre elas:

### Resultado da partida

```text
Vitória Mandante
Empate
Vitória Visitante
```

### Resultado do clube

Para análises no nível de cada equipe:

```text
Vitória
Empate
Derrota
```

### Indicadores de partida

```text
Ano
Gols da partida
Saldo do mandante
Pontos do mandante
Pontos do visitante
```

Essas variáveis permitem transformar os dados brutos em informações diretamente utilizáveis nas análises.

---

# 📊 Dashboard

O dashboard será desenvolvido no **Power BI**, utilizando os dados tratados e modelados.

## Página 1 — Visão Geral

Principais indicadores:

* Total de partidas
* Total de gols
* Média de gols por partida
* Número de clubes
* Total de cartões
* Arrecadação
* Evolução dos gols ao longo dos anos

Objetivo:

> Apresentar uma visão geral do Campeonato Brasileiro e permitir uma leitura rápida da evolução dos principais indicadores.

---

## Página 2 — Performance dos Clubes

Análises relacionadas ao desempenho das equipes:

* Jogos disputados
* Vitórias
* Empates
* Derrotas
* Gols marcados
* Gols sofridos
* Saldo de gols
* Pontos
* Média de gols
* Indicadores ofensivos

Também serão exploradas relações como:

```text
Finalizações × Gols
Posse de bola × Resultado
Chutes no alvo × Gols
```

---

## Página 3 — O que influencia o resultado?

Esta página busca investigar a relação entre indicadores estatísticos e os resultados das partidas.

Possíveis análises:

* Posse de bola por resultado
* Finalizações por resultado
* Chutes no alvo por resultado
* Escanteios por resultado
* Precisão de passes por resultado
* Faltas por resultado

O objetivo não é afirmar que determinado indicador **causa** um resultado, mas investigar quais padrões aparecem nos dados.

---

## Página 4 — Eventos das partidas

Análise dos acontecimentos ao longo dos jogos.

Possíveis visualizações:

* Gols por minuto
* Cartões por minuto
* Gols por período da partida
* Cartões por período
* Distribuição dos eventos ao longo dos jogos

Exemplo de divisão:

```text
0–15
16–30
31–45
46–60
61–75
76–90+
```

---

# 📈 Indicadores

Entre os indicadores que serão desenvolvidos estão:

### Partidas

```text
Total de partidas
Total de clubes
Partidas por temporada
```

### Gols

```text
Total de gols
Média de gols por partida
Gols do mandante
Gols do visitante
```

### Desempenho

```text
Vitórias
Empates
Derrotas
Pontos
Saldo de gols
```

### Estatísticas

```text
Chutes
Chutes no alvo
Posse de bola
Passes
Precisão de passes
Escanteios
Faltas
Impedimentos
```

### Disciplina

```text
Cartões amarelos
Cartões vermelhos
Cartões por partida
```

---

# 🧠 Principais conceitos aplicados

Durante o desenvolvimento são utilizados conceitos de:

* Python para análise de dados
* Pandas
* NumPy
* ETL
* Data Cleaning
* Exploratory Data Analysis (EDA)
* Modelagem dimensional
* Relacionamentos entre tabelas
* Granularidade de dados
* Data Visualization
* Power BI
* DAX
* KPIs
* Storytelling com dados
* Análise estatística descritiva

---

# 🛠️ Tecnologias utilizadas

| Tecnologia     | Utilização                |
| -------------- | ------------------------- |
| 🐍 Python      | Tratamento e análise      |
| 🐼 Pandas      | Manipulação dos dados     |
| 🔢 NumPy       | Transformações e cálculos |
| 📊 Matplotlib  | Análise exploratória      |
| 📈 Power BI    | Dashboard e visualização  |
| 🧮 DAX         | Métricas e indicadores    |
| 🗃️ Git/GitHub | Versionamento e portfólio |

---

# 🚀 Próximos passos

O projeto está sendo desenvolvido de forma incremental.

### Etapa 1 — Entendimento dos dados

* [x] Carregar os datasets
* [x] Identificar tabelas e granularidades
* [x] Inspecionar colunas
* [x] Entender os relacionamentos

### Etapa 2 — Tratamento

* [x] Converter datas
* [x] Criar ano
* [x] Criar resultado da partida
* [x] Criar indicadores básicos
* [ ] Verificar valores ausentes
* [ ] Verificar inconsistências
* [ ] Padronizar categorias

### Etapa 3 — Modelagem

* [x] Criar dimensão de clubes
* [ ] Preparar tabela de estatísticas
* [ ] Preparar tabela de gols
* [ ] Preparar tabela de cartões
* [ ] Estruturar modelo dimensional

### Etapa 4 — Análise exploratória

* [ ] Analisar distribuição dos resultados
* [ ] Analisar gols
* [ ] Analisar desempenho dos clubes
* [ ] Explorar estatísticas das partidas
* [ ] Investigar relações entre indicadores

### Etapa 5 — Power BI

* [ ] Importar dados tratados
* [ ] Criar relacionamentos
* [ ] Criar medidas DAX
* [ ] Construir dashboard
* [ ] Criar filtros e interações
* [ ] Revisar experiência visual

### Etapa 6 — Portfólio

* [ ] Documentar metodologia
* [ ] Registrar principais insights
* [ ] Adicionar imagens do dashboard
* [ ] Finalizar README
* [ ] Publicar no GitHub
* [ ] Criar publicação no LinkedIn

---

# 💡 Resultado esperado

Ao final, o projeto deverá apresentar uma solução completa de análise de dados capaz de transformar dados históricos do Campeonato Brasileiro em **informação analítica e visualizações interativas**.

Além do dashboard final, o projeto documentará todo o processo de construção, desde a exploração dos dados brutos até a geração dos indicadores.

---

# 👨‍💻 Autor

**Gustavo da Silva Pires**

Projeto desenvolvido como parte do desenvolvimento de competências em:

**Data Analytics • Python • Power BI • SQL • Data Science • Inteligência Artificial**

---

## 📌 Status

🟡 **Em desenvolvimento**

O projeto está sendo construído passo a passo, com foco tanto no resultado final quanto no aprendizado das técnicas utilizadas durante o processo.
