import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from bcb import sgs
import investpy
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic, IBOV, IMOB e IFIX - Comparativo", layout="wide")

# Título
st.title("Taxa Selic, Índice Bovespa, Índice Imobiliário e IFIX - Comparativo")

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

# Função para carregar os dados do IBOV (mantido com yfinance)
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

# Função para carregar os dados do IMOB (usando investpy)
@st.cache_data
def carregar_dados_imob():
    try:
        imob = investpy.get_index_historical_data(
            index='IMOB',
            country='Brazil',
            from_date='01/01/2010',
            to_date=date.today().strftime('%d/%m/%Y')
        )
        imob = imob[['Close']].rename(columns={'Close': 'IMOB'})
        imob.reset_index(inplace=True)
        imob.columns = ['Date', 'IMOB']
        st.write("Primeiras linhas do IMOB (investpy):", imob.head())  # Depuração
        return imob
    except Exception as e:
        st.error(f"Erro ao carregar dados do IMOB com investpy: {e}")
        return pd.DataFrame()

# Função para carregar os dados do IFIX (usando investpy)
@st.cache_data
def carregar_dados_ifix():
    try:
        ifix = investpy.get_index_historical_data(
            index='IFIX',
            country='Brazil',
            from_date='01/01/2010',
            to_date=date.today().strftime('%d/%m/%Y')
        )
        ifix = ifix[['Close']].rename(columns={'Close': 'IFIX'})
        ifix.reset_index(inplace=True)
        ifix.columns = ['Date', 'IFIX']
        st.write("Primeiras linhas do IFIX (investpy):", ifix.head())  # Depuração
        return ifix
    except Exception as e:
        st.error(f"Erro ao carregar dados do IFIX com investpy: {e}")
        return pd.DataFrame()

# Carregar os dados
df_selic = carregar_dados_selic()
df_ibov = carregar_dados_ibov()
df_imob = carregar_dados_imob()
df_ifix = carregar_dados_ifix()

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

# Exibir o IFIX atual
st.subheader("Índice de Fundos Imobiliários (IFIX)")
if not df_ifix.empty:
    try:
        ultimo_ifix = float(df_ifix['IFIX'].iloc[-1])
        if not pd.isna(ultimo_ifix):
            ultima_data_ifix = df_ifix['Date'].iloc[-1].strftime('%d/%m/%Y')
            st.write(f"IFIX Atual: {ultimo_ifix:.2f} pontos (Data: {ultima_data_ifix})")
        else:
            st.write("IFIX Atual: Dados indisponíveis (valor ausente)")
    except Exception as e:
        st.write(f"IFIX Atual: Erro ao processar dados ({e})")
else:
    st.write("IFIX Atual: Dados indisponíveis")

# Combinar os dados para o gráfico comparativo
if not df_selic.empty and not df_ibov.empty:
    # Converter os DataFrames para o mesmo formato de índice que df_selic
    df_ibov_indexed = df_ibov.set_index('Date')
    df_imob_indexed = df_imob.set_index('Date') if not df_imob.empty else pd.DataFrame()
    df_ifix_indexed = df_ifix.set_index('Date') if not df_ifix.empty else pd.DataFrame()
    
    # Combinar os DataFrames com alinhamento por datas
    df_comparacao = df_selic.join(df_ibov_indexed, how='inner')
    if not df_imob_indexed.empty:
        df_comparacao = df_comparacao.join(df_imob_indexed, how='inner')
    if not df_ifix_indexed.empty:
        df_comparacao = df_comparacao.join(df_ifix_indexed, how='inner')
    
    # Criar o gráfico comparativo
    fig = go.Figure()

    # Linha da Selic (eixo Y esquerdo)
    fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['Taxa Selic (%)'],
                             name='Selic (%)', line=dict(color='blue'), yaxis='y1'))

    # Linha do IBOV (eixo Y direito)
    fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['IBOV'],
                             name='IBOV (pontos)', line=dict(color='green'), yaxis='y2'))

    # Linha do IMOB (eixo Y direito, se disponível)
    if 'IMOB' in df_comparacao.columns:
        fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['IMOB'],
                                 name='IMOB (pontos)', line=dict(color='orange'), yaxis='y2'))

    # Linha do IFIX (eixo Y direito, se disponível)
    if 'IFIX' in df_comparacao.columns:
        fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['IFIX'],
                                 name='IFIX (pontos)', line=dict(color='purple'), yaxis='y2'))

    # Configuração do layout com dois eixos Y
    fig.update_layout(
        title="Comparativo: Taxa Selic, IBOV, IMOB e IFIX desde 2010",
        xaxis_title="Data",
        yaxis=dict(title="Taxa Selic (%)", side="left", color="blue"),
        yaxis2=dict(title="Índices (pontos)", side="right", overlaying="y", color="green"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Dados insuficientes para criar o gráfico comparativo.")

# Fonte
st.markdown("Fontes: Banco Central do Brasil (SGS), Yahoo Finance (IBOV) e Investing.com (IMOB, IFIX via investpy)")
