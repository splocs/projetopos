import streamlit as st
import pandas as pd
from bcb import sgs
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic e IBOV - Histórico e Atual", layout="wide")

# Título
st.title("Taxa Selic e Índice Bovespa - Histórico e Atual")

# Função para carregar os dados da Selicimport streamlit as st
import pandas as pd
from bcb import sgs
import yfinance as yf
import plotly.graph_objects as go
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

# Plotar gráfico comparativo da Selic e do IBOV
if not df_selic.empty and not df_ibov.empty:
    try:
        # Resetar o índice para garantir que ambos tenham o mesmo formato
        df_selic_reset = df_selic.reset_index()
        df_ibov_reset = df_ibov.reset_index()

        # Alinhar as datas de Selic e IBOV
        df_combined = pd.merge(df_selic_reset, df_ibov_reset, left_on='Date', right_on='Date', how='inner')

        # Criar o gráfico com duas linhas: uma para a Selic e outra para o IBOV
        fig = go.Figure()

        # Linha da Selic
        fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined['Taxa Selic (%)'], 
                                 mode='lines', name='Taxa Selic (%)', line=dict(color='blue')))

        # Linha do IBOV
        fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined['IBOV'], 
                                 mode='lines', name='Índice Bovespa (IBOV)', line=dict(color='green')))

        # Adicionar títulos e configurações ao gráfico
        fig.update_layout(
            title="Comparativo Histórico entre Taxa Selic e Índice Bovespa (IBOV)",
            xaxis_title="Data",
            yaxis_title="Taxa Selic (%)",
            template="plotly_white",
            yaxis2=dict(
                title="Índice Bovespa (IBOV)",
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0.01, y=0.99)
        )

        # Exibir o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico comparativo: {e}")
else:
    st.warning("Não há dados suficientes para criar o gráfico comparativo.")

# Fonte
st.markdown("Fonte

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

# Plotar gráfico comparativo da Selic e do IBOV
if not df_selic.empty and not df_ibov.empty:
    try:
        # Alinhar as datas de Selic e IBOV
        df_combined = pd.merge(df_selic, df_ibov, left_index=True, right_index=True, how='inner')

        # Criar o gráfico com duas linhas: uma para a Selic e outra para o IBOV
        fig = go.Figure()

        # Linha da Selic
        fig.add_trace(go.Scatter(x=df_combined.index, y=df_combined['Taxa Selic (%)'], 
                                 mode='lines', name='Taxa Selic (%)', line=dict(color='blue')))

        # Linha do IBOV
        fig.add_trace(go.Scatter(x=df_combined.index, y=df_combined['IBOV'], 
                                 mode='lines', name='Índice Bovespa (IBOV)', line=dict(color='green')))

        # Adicionar títulos e configurações ao gráfico
        fig.update_layout(
            title="Comparativo Histórico entre Taxa Selic e Índice Bovespa (IBOV)",
            xaxis_title="Data",
            yaxis_title="Taxa Selic (%)",
            template="plotly_white",
            yaxis2=dict(
                title="Índice Bovespa (IBOV)",
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0.01, y=0.99)
        )

        # Exibir o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico comparativo: {e}")
else:
    st.warning("Não há dados suficientes para criar o gráfico comparativo.")

# Fonte
st.markdown("Fontes: Banco Central do Brasil (SGS) e Yahoo Finance")
