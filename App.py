import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Função para pegar a taxa Selic histórica
def get_selic_historical():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv"
    response = requests.get(url)
    data = response.text.splitlines()
    df = pd.DataFrame([line.split(';') for line in data], columns=['Date', 'Selic'])
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Selic'] = df['Selic'].str.replace(',', '.').astype(float)
    return df

# Função para pegar a taxa Selic atual
def get_selic_current():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv&dataInicial=01/01/2025&dataFinal=01/01/2025"
    response = requests.get(url)
    data = response.text.splitlines()
    last_value = data[-1].split(';')[1]  # último valor da lista
    return float(last_value.replace(',', '.'))

# Cabeçalho do app
st.title("Taxa Selic Atual e Histórica")

# Pegando a taxa Selic atual
selic_atual = get_selic_current()
st.subheader(f"Taxa Selic Atual: {selic_atual:.2f}%")

# Pegando o histórico da taxa Selic
df_selic = get_selic_historical()

# Exibindo os dados históricos em tabela
st.subheader("Histórico da Taxa Selic")
st.dataframe(df_selic)

# Gráfico da taxa Selic histórica
st.subheader("Gráfico Histórico da Taxa Selic")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_selic['Date'], df_selic['Selic'], color='blue')
ax.set_xlabel('Data')
ax.set_ylabel('Taxa Selic (%)')
ax.set_title('Histórico da Taxa Selic')
st.pyplot(fig)
