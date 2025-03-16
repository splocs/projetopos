import streamlit as st
import pandas as pd
from bcb import sgs
import plotly.express as px
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic - Histórico e Atual", layout="wide")

# Título
st.title("Taxa Selic - Histórico e Atual")

# Função para carregar os dados da Selic
@st.cache_data
def carregar_dados_selic():
    try:
        selic = sgs.get({'Selic': 432}, start='2010-01-01', end=date.today())
        selic = selic.rename(columns={'Selic': 'Taxa Selic (%)'})
        return selic
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Carregar os dados
df_selic = carregar_dados_selic()

# Verificar se há dados
if df_selic.empty:
    st.warning("Nenhum dado disponível.")
    st.stop()

# Exibir a Selic atual
ultima_taxa = df_selic['Taxa Selic (%)'].iloc[-1]
ultima_data = df_selic.index[-1].strftime('%d/%m/%Y')
st.subheader(f"Selic Atual: {ultima_taxa:.2f}%")
st.write(f"Data: {ultima_data}")

# Gráfico simples do histórico
st.subheader("Histórico da Selic")
fig = px.line(df_selic, x=df_selic.index, y='Taxa Selic (%)', 
              title="Evolução da Taxa Selic")
st.plotly_chart(fig, use_container_width=True)

# Fonte
st.markdown("Fonte: Banco Central do Brasil (SGS)")
