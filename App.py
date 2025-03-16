import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from bcb import sgs
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic, IBOV e IMOB - Histórico e Atual", layout="wide")

# Título
st.title("Taxa Selic, Índice Bovespa e Índice Imobiliário - Histórico e Atual")

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
        ibov = ibov[['Close']]
        ibov.reset_index(inplace=True)
        ibov.columns = ['Date', 'IBOV']
        return ibov
    except Exception as e:
        st.error(f"Erro ao carregar dados do IBOV: {e}")
        return pd.DataFrame()

# Função para carregar os dados do IMOB
@st.cache_data
def carregar_dados_imob():
    try:
        imob = yf.download('^IMOB', start='2010-01-01', end=date.today(), progress=False)
        imob = imob[['Close']]
        imob.reset_index(inplace=True)
        imob.columns = ['Date', 'IMOB']
        return imob
    except Exception as e:
        st.error(f"Erro ao carregar dados do IMOB: {e}")
        return pd.DataFrame()

# Carregar os dados
df_selic = carregar_dados_selic()
df_ibov = carregar_dados_ibov()
df_imob = carregar_dados_imob()

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
            ultima_data_ibov = df_ibov['Date'].iloc[-1].strftime('%d/%m/%Y')
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
        fig_ibov = px.line(df_ibov, x='Date', y='IBOV', 
                           title="Histórico do Índice Bovespa desde 2010")
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

# Exibir o IMOB atual
st.subheader("Índice Imobiliário (IMOB)")
if not df_imob.empty:
    try:
        ultimo_imob = float(df_imob['IMOB'].iloc[-1])
        if not pd.isna(ultimo_imob):
            ultima_data_imob = df_imob['Date'].iloc[-1].strftime('%d/%m/%Y')
            st.write(f"IMOB Atual: {ultimo_imob:.2f} pontos (Data: {ultima_data_imob})")
        else:
            st.write("IMOB Atual: Dados indisponíveis (valor ausente)")
    except Exception as e:
        st.write(f"IMOB Atual: Erro ao processar dados ({e})")
else:
    st.write("IMOB Atual: Dados indisponíveis")

# Gráfico do IMOB
if not df_imob.empty:
    try:
        fig_imob = px.line(df_imob, x='Date', y='IMOB', 
                           title="Histórico do Índice Imobiliário desde 2010")
        fig_imob.update_layout(
            xaxis_title="Data",
            yaxis_title="IMOB (pontos)",
            template="plotly_white"
        )
        st.plotly_chart(fig_imob, use_container_width=True)
    except Exception as e:
        st.warning(f"Erro ao criar gráfico do IMOB: {e}")
else:
    st.warning("Nenhum dado disponível para o gráfico do IMOB.")

# Fonte
st.markdown("Fontes: Banco Central do Brasil (SGS) e Yahoo Finance")
