import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Função para pegar a taxa Selic histórica
def get_selic_historical():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text.splitlines()
        df = pd.DataFrame([line.split(';') for line in data], columns=['Date', 'Selic'])

        # Converter as datas automaticamente sem especificar o formato
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Limpar os dados
        df['Selic'] = df['Selic'].str.replace(',', '.').astype(float)
        df.dropna(inplace=True)  # Remove linhas com valores NaT (erro na data)
        
        return df
    else:
        st.error(f"Erro ao acessar os dados históricos da Selic: {response.status_code}")
        return pd.DataFrame()

# Função para pegar a taxa Selic atual
def get_selic_current():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv&dataInicial=01/01/2025&dataFinal=01/01/2025"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text.splitlines()
        if len(data) > 1:
            last_value = data[-1].split(';')[1]  # último valor da lista
            return float(last_value.replace(',', '.'))
        else:
            st.error("Não foi possível obter a taxa Selic atual.")
            return None
    else:
        st.error(f"Erro ao acessar a taxa Selic atual: {response.status_code}")
        return None

# Cabeçalho do app
st.title("Taxa Selic Atual e Histórica")

# Pegando a taxa Selic atual
selic_atual = get_selic_current()
if selic_atual is not None:
    st.subheader(f"Taxa Selic Atual: {selic_atual:.2f}%")

# Pegando o histórico da taxa Selic
df_selic = get_selic_historical()
if not df_selic.empty:
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
