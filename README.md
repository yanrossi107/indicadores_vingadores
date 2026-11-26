# Indicadores Vingadores

Dashboard em Streamlit com indicadores sobre os heróis Vingadores (`data/avengers.csv`).

## Como rodar

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

Depois, abra http://localhost:8501.

## Estrutura

- `app.py`: página do dashboard (filtros, KPIs, gráficos e tabela)
- `src/data.py`: carga e limpeza do CSV
- `data/avengers.csv`: base de dados
