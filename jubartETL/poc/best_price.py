import streamlit as st
import pandas as pd
import numpy as np
# import plotly.express as px

st.set_page_config(layout="wide")

df_filtrado = pd.read_csv('../dataset/sm_total.csv')


st.title('Produtos em ofertas')


all_val = 'Todos'
# adcionando as categorias como filtro lateral
categoria_list = np.insert(df_filtrado["categoria"].unique(), 0, all_val)
source = st.sidebar.selectbox("categoria", categoria_list, index=0)
if source != all_val:
    df_filtrado = df_filtrado[df_filtrado["categoria"] == source]

# adcionando os super mercados como filtro lateral
supermarket_list = np.insert(df_filtrado["supermarket"].unique(), 0, all_val)
source = st.sidebar.selectbox("Super mercado", supermarket_list, index=0)
if source != all_val:
    df_filtrado = df_filtrado[df_filtrado["supermarket"] == source]

# filtro nos produtos
filtro = st.text_input('Digite o nome do produto:')
if filtro:
    df_filtrado = df_filtrado[df_filtrado['nome'].astype(str).str.contains(filtro, case=False)]

st.write(f"Número de registros: {len(df_filtrado)}")

st.dataframe(df_filtrado[['nome', 'preco', 'gramagem', 'supermarket', 'data_ini',
                          'data_fim']].set_index(df_filtrado.columns[0]))
