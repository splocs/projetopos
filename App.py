import streamlit as st
import pandas as pd
from bcb import sgs
import yfinance as yf
import plotly.express as px
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic e IBOV - Histórico e Atual", layout="wide")

# Título
st.title("Taxa Selic e Índice Bovespa - Histórico e Atual")

# Função para carregar os dados da Selic
@st.cache_data
def carregar_dados_selic():
    try:
        selic = sgs.get({'Selic': 432}, start='2010-01-01', end=date.today())
        selic = selic.rename(columns={'Selic': 'Taxa Selic (%)'})
        return selic
    except Exception as e:
        st.error(f"Erro ao carregar dados da Selic: {e}")
        return pd.DataFrame()

# Função para carregar os dados do IBOV
@st.cache_data
def carregar_dados_ibov():
    try:
        ibov = yf.download('^BVSP', start='2010-01-01', end=date.today(), progress=False)
        ibov = ibov[['Close']].rename(columns={'Close': 'IBOV'})
        return ibov
    except Exception as e:
        st.error(f"Erro ao carregar dados do IBOV: {e}")
        return pd.DataFrame()

# Carregar os dados
df_selic = carregar_dados_selic()
df_ibov = carregar_dados_ibov()

# Exibir a Selic atual
st.subheader("Taxa Selic")
if not df_selic.empty:
    try:
        ultima_taxa = float(df_selic['Taxa Selic (%)'].iloc[-1])
        if not pd.isna(ultima_taxa):
            ultima_data = df_selic.index[-1].strftime('%d/%m/%Y')
            st.write(f"Selic Atual: {ultima_taxa:.2f}% (Data: {ultima_data})")
        else:
            st.write("Selic Atual: Dados indisponíveis (valor ausente)")
    except Exception as e:
        st.write(f"Selic Atual: Erro ao processar dados ({e})")
else:
    st.write("Selic Atual: Dados indisponíveis")

# Gráfico da Selic
if not df_selic.empty:
    try:
        fig_selic = px.line(df_selic, x=df_selic.index, y='Taxa Selic (%)', 
                            title="Histórico da Taxa Selic")
        fig_selic.update_layout(
            xaxis_title="Data",
            yaxis_title="Taxa Selic (%)",
            template="plotly_white"
        )
        st.plotly_chart(fig_selic, use_container_width=True)
    except Exception as e:
        st.warning(f"Erro ao criar gráfico da Selic: {e}")
else:
    st.warning("Nenhum dado disponível para o gráfico da Selic.")

# Exibir o IBOV atual
st.subheader("Índice Bovespa (IBOV)")
if not df_ibov.empty:
    try:
        ultimo_ibov = float(df_ibov['IBOV'].iloc[-1])
        if not pd.isna(ultimo_ibov):
            ultima_data_ibov = df_ibov.index[-1].strftime('%d/%m/%Y')
            st.write(f"IBOV Atual: {ultimo_ibov:.2f} pontos (Data: {ultima_data_ibov})")
        else:
            st.write("IBOV Atual: Dados indisponíveis (valor ausente)")
    except Exception as e:
        st.write(f"IBOV Atual: Erro ao processar dados ({e})")
else:
    st.write("IBOV Atual: Dados indisponíveis")

# Gráfico do IBOV
if not df_ibov.empty:
    try:
        # Resetar o índice para garantir que Plotly use colunas explícitas
        df_ibov_plot = df_ibov.reset_index()
        fig_ibov = px.line(df_ibov_plot, x='Date', y='IBOV', 
                           title="Histórico do Índice Bovespa")
        fig_ibov.update_layout(
            xaxis_title="Data",
            yaxis_title="IBOV (pontos)",
            template="plotly_white"
        )
        st.plotly_chart(fig_ibov, use_container_width=True)
    except Exception as e:
        st.warning(f"Erro ao criar gráfico do IBOV: {e}")
else:
    st.warning("Nenhum dado disponível para o gráfico do IBOV.")

# Fonte
st.markdown("Fontes: Banco Central do Brasil (SGS) e Yahoo Finance")
