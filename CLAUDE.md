# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Dashboard de indicadores sobre os heróis Vingadores, a partir de `data/avengers.csv`. O foco atual é a base do projeto, não a estética. O usuário escreve em português; responda em português.

Ainda não há testes nem lint configurados.

## Stack e comandos

Python 3.13 + Streamlit + pandas + Plotly (veja `requirements.txt`). Ambiente Windows; use o venv local `.venv`.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\streamlit run app.py   # http://localhost:8501
```

`.claude/launch.json` tem a configuração `dashboard` para abrir o app no browser pane.

## Arquitetura

- `src/data.py` → `load_heroes()` é a única porta de entrada dos dados: lê o CSV, renomeia as colunas para português (`nome`, `aparicoes`, `ativo`, `genero`, `ano_entrada`, `categoria`, ...) e cria colunas derivadas (`mortes`, `retornos`, `ja_morreu`, `decada`). Toda nova limpeza ou métrica por herói vai aqui, não no app.
- `app.py` → página Streamlit única: chama `load_heroes()` com `st.cache_data`, aplica os filtros da sidebar em um DataFrame `f` e desenha KPIs, gráficos Plotly e a tabela a partir de `f`.
- Streamlit ≥ 1.5x: use `width="stretch"`, não `use_container_width` (obsoleto). A telemetria está desligada em `.streamlit/config.toml`.

## Particularidades do CSV (`data/avengers.csv`)

- **Encoding `latin-1`**: ler como UTF-8 quebra. Use `pd.read_csv(path, encoding="latin-1")`.
- São 173 linhas, uma por herói. Colunas principais: `Name/Alias`, `Appearances`, `Current?` (YES/NO), `Gender`, `Year` (ano de entrada), `Years since joining`, `Honorary` (Full, Honorary, Academy, Probationary).
- A coluna `Full/Reserve Avengers Intro` vem em formato `Mon-YY` (ex.: `Sep-63`). Prefira a coluna `Year` para análises temporais.
- `Year = 1900` é um valor de preenchimento para os 14 heróis sem data de entrada (Academy/Probationary). `load_heroes()` converte esse valor em nulo (`Int64`), então trate `ano_entrada`/`decada` como possivelmente vazios.
- `Death1..Death5` / `Return1..Return5` são YES/NO, e uma célula vazia significa que o evento não aconteceu. O número de mortes de um herói é a contagem de `Death*` igual a YES.
- Há nomes com aspas duplas escapadas (ex.: `Henry Jonathan ""Hank"" Pym`) e um campo `Notes` em texto livre.
