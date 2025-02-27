import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";")

# Contar a frequência de UBS por estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

# Criar o dashboard
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# Gráfico de barras
grafico = px.bar(df_freq, x='Estado', y='Frequência', 
                 title='Frequência de UBS por Estado', 
                 labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
                 text_auto=True,
                 color='Estado')

st.plotly_chart(grafico)

# Filtro para estados específicos
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)

####################################################################################################################
# Corrigir o formato das coordenadas, pois com "," não é possivel encontrar o local no mapa
df["LATITUDE"] = df["LATITUDE"].astype(str).str.replace(",", ".").astype(float)
df["LONGITUDE"] = df["LONGITUDE"].astype(str).str.replace(",", ".").astype(float)


st.title("Mapa Interativo das Unidades Básicas de Saúde (UBS)")

estados = st.multiselect("Selecione os estados", df['Nome_UF'].unique())

df_filtrado = df[df['Nome_UF'].isin(estados)] if estados else df

fig = px.scatter_mapbox(
    df_filtrado, lat="LATITUDE", lon="LONGITUDE", hover_name="NOME",
    color_discrete_sequence=["fuchsia"], zoom=5, height=600
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

st.plotly_chart(fig)
####################################################################################################################
st.title("Distribuição de UBS por Estado")
df_pizza = df["Nome_UF"].value_counts().reset_index()
df_pizza.columns = ["Estado", "Percentual"]

fig_pizza = px.pie(df_pizza, names="Estado", values="Percentual", title="Percentual de UBS por Estado")

st.plotly_chart(fig_pizza)
####################################################################################################################
st.title("Histograma da Quantidade de UBS por Município")
df_histogram = df["Nome_Município"].value_counts().reset_index()
df_histogram.columns = ["Município", "Quantidade"]

min_ubs = st.slider("Número mínimo de UBS por município", 
                    min_value=int(df_histogram["Quantidade"].min()), 
                    max_value=int(df_histogram["Quantidade"].max()), 
                    value= int(df_histogram["Quantidade"].min()))

df_histogram_filtrado = df_histogram[df_histogram["Quantidade"] >= min_ubs]

fig_histogram = px.histogram(df_histogram_filtrado, x="Município", y="Quantidade", title="Quantidade de UBS por Município", color="Município")
st.plotly_chart(fig_histogram)
####################################################################################################################