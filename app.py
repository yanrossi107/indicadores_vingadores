import plotly.express as px
import streamlit as st

from src.data import load_heroes

st.set_page_config(page_title="Indicadores Vingadores", layout="wide")


@st.cache_data
def get_data():
    return load_heroes()


df = get_data()

# --- Filtros ---------------------------------------------------------------
st.sidebar.header("Filtros")
generos = st.sidebar.multiselect("Gênero", sorted(df["genero"].dropna().unique()), default=None)
categorias = st.sidebar.multiselect("Categoria", sorted(df["categoria"].dropna().unique()), default=None)
so_ativos = st.sidebar.checkbox("Somente ativos", value=False)
ano_min, ano_max = int(df["ano_entrada"].min()), int(df["ano_entrada"].max())
anos = st.sidebar.slider("Ano de entrada", ano_min, ano_max, (ano_min, ano_max))
incluir_sem_ano = st.sidebar.checkbox("Incluir heróis sem ano de entrada", value=True)

no_periodo = df["ano_entrada"].between(*anos).fillna(False)
f = df[no_periodo | (incluir_sem_ano & df["ano_entrada"].isna())]
if generos:
    f = f[f["genero"].isin(generos)]
if categorias:
    f = f[f["categoria"].isin(categorias)]
if so_ativos:
    f = f[f["ativo"]]

# --- KPIs ------------------------------------------------------------------
st.title("Indicadores Vingadores")

if f.empty:
    st.warning("Nenhum herói encontrado com os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Heróis", len(f))
c2.metric("Ativos", int(f["ativo"].sum()))
c3.metric("Já morreram", f"{f['ja_morreu'].mean():.0%}")
c4.metric("Média de aparições", f"{f['aparicoes'].mean():.0f}")

# --- Gráficos --------------------------------------------------------------
col1, col2 = st.columns(2)

top = f.nlargest(10, "aparicoes").sort_values("aparicoes")
col1.subheader("Top 10 por aparições")
col1.plotly_chart(px.bar(top, x="aparicoes", y="nome", orientation="h"), width="stretch")

col2.subheader("Entradas por década")
por_decada = f.groupby("decada").size().reset_index(name="herois")
col2.plotly_chart(px.bar(por_decada, x="decada", y="herois"), width="stretch")

col3, col4 = st.columns(2)

col3.subheader("Gênero")
col3.plotly_chart(px.pie(f, names="genero"), width="stretch")

col4.subheader("Mortes por herói")
mortes = f.groupby("mortes").size().reset_index(name="herois")
col4.plotly_chart(px.bar(mortes, x="mortes", y="herois"), width="stretch")

# --- Tabela ----------------------------------------------------------------
st.subheader("Heróis")
st.dataframe(
    f[["nome", "aparicoes", "ativo", "genero", "ano_entrada", "categoria", "mortes", "retornos"]]
    .sort_values("aparicoes", ascending=False),
    hide_index=True,
    width="stretch",
)
