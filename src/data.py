"""Carga e limpeza da base de heróis (data/avengers.csv)."""

from pathlib import Path
from urllib.parse import unquote

import pandas as pd

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "avengers.csv"

RENAME = {
    "URL": "url",
    "Name/Alias": "nome",
    "Appearances": "aparicoes",
    "Current?": "ativo",
    "Gender": "genero",
    "Year": "ano_entrada",
    "Years since joining": "anos_desde_entrada",
    "Honorary": "categoria",
    "Notes": "notas",
}

DEATH_COLS = [f"Death{i}" for i in range(1, 6)]
RETURN_COLS = [f"Return{i}" for i in range(1, 6)]
UNKNOWN_YEAR = 1900
EARTH_SUFFIX = r"_\(Earth-\d+\)#?$"


def _nome_pela_url(url: pd.Series) -> pd.Series:
    """Deriva o nome do último segmento da URL (ex.: `Dinah_Soar_(Earth-616)#` -> `Dinah Soar`)."""
    segmento = url.str.rstrip("/").str.rsplit("/", n=1).str[-1]
    segmento = segmento.map(unquote, na_action="ignore")
    nome = segmento.str.replace(EARTH_SUFFIX, "", regex=True).str.replace("_", " ").str.strip()
    return nome.replace("", pd.NA)


def load_heroes(path: Path = CSV_PATH) -> pd.DataFrame:
    """Lê o CSV (latin-1) e devolve um DataFrame limpo, com colunas em português."""
    raw = pd.read_csv(path, encoding="latin-1")

    is_yes = raw[DEATH_COLS + RETURN_COLS].eq("YES")
    df = raw[list(RENAME)].rename(columns=RENAME)

    # Heróis sem Name/Alias no CSV: o nome é derivado da URL; "(sem nome)" fica só como fallback.
    df["nome"] = df["nome"].fillna(_nome_pela_url(df["url"])).fillna("(sem nome)").str.strip()
    df["ativo"] = df["ativo"].eq("YES")
    df["genero"] = df["genero"].str.capitalize().map({"Male": "Masculino", "Female": "Feminino"})
    df["mortes"] = is_yes[DEATH_COLS].sum(axis=1)
    df["retornos"] = is_yes[RETURN_COLS].sum(axis=1)
    df["ja_morreu"] = df["mortes"] > 0
    # 1900 é um valor de preenchimento para heróis sem data de entrada (Academy/Probationary).
    sem_ano = df["ano_entrada"].eq(UNKNOWN_YEAR)
    df["ano_entrada"] = df["ano_entrada"].mask(sem_ano).astype("Int64")
    df["anos_desde_entrada"] = df["anos_desde_entrada"].mask(sem_ano).astype("Int64")
    df["decada"] = df["ano_entrada"] // 10 * 10
    return df
