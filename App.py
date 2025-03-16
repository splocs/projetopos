import streamlit as st
import pandas as pd
from bcb import sgs
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

# Configuração do Streamlit
st.set_page_config(page_title="Selic vs IBOV - Histórico e Atual", layout="wide")

# Título
st.title("Taxa Selic vs Índice Bovespa - Comparação")

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

# Verificar se há dados válidos
if df_selic.empty or df_ibov.empty:
    st.warning("Dados insuficientes para exibição. Verifique os logs para mais detalhes.")
    st.stop()

# Exibir a Selic atual
ultima_taxa = df_selic['Taxa Selic (%)'].iloc[-1]
if pd.isna(ultima_taxa):
    st.subheader("Selic Atual: Dados indisponíveis")
else:
    ultima_data = df_selic.index[-1].strftime('%d/%m/%Y')
    st.subheader(f"Selic Atual: {ultima_taxa:.2f}%")
    st.write(f"Data: {ultima_data}")

# Exibir o IBOV atual
ultimo_ibov = df_ibov['IBOV'].iloc[-1]
if pd.isna(ultimo_ibov):
    st.subheader("IBOV Atual: Dados indisponíveis")
else:
    ultima_data_ibov = df_ibov.index[-1].strftime('%d/%m/%Y')
    st.subheader(f"IBOV Atual: {ultimo_ibov:.2f} pontos")
    st.write(f"Data: {ultima_data_ibov}")

# Combinar os dados em um único DataFrame para alinhar as datas
df_comparacao = df_selic.join(df_ibov, how='inner')

# Verificar se o DataFrame combinado tem dados
if df_comparacao.empty:
    st.warning("Nenhum dado disponível para o período comum entre Selic e IBOV.")
    st.stop()

# Gráfico com duas linhas (Selic e IBOV)
st.subheader("Histórico: Selic vs IBOV")
fig = go.Figure()

# Linha da Selic (eixo Y esquerdo)
fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['Taxa Selic (%)'],
                         name='Selic (%)', line=dict(color='blue'), yaxis='y1'))

# Linha do IBOV (eixo Y direito)
fig.add_trace(go.Scatter(x=df_comparacao.index, y=df_comparacao['IBOV'],
                         name='IBOV (pontos)', line=dict(color='green'), yaxis='y2'))

# Configuração do layout com dois eixos Y
fig.update_layout(
    title="Evolução da Taxa Selic e Índice Bovespa",
    xaxis_title="Data",
    yaxis=dict(title="Taxa Selic (%)", side="left", color="blue"),
    yaxis2=dict(title="IBOV (pontos)", side="right", overlaying="y", color="green"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Fonte
st.markdown("Fontes: Banco Central do Brasil (SGS) e Yahoo Finance")
