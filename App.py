import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
from functools import lru_cache
import logging

# Configuração de logging para monitoramento de erros
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Plotos.com.br",
    page_icon="FAV.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Plotos - Análise Financeira Avançada"
    }
)

# Cache para dados que não mudam frequentemente
@lru_cache(maxsize=128)
def pegar_dados_acoes():
    """Carrega lista de ações de um CSV hospedado no GitHub."""
    try:
        path = 'https://raw.githubusercontent.com/splocs/meu-repositorio/main/acoes.csv'
        df = pd.read_csv(path, delimiter=';', encoding='utf-8')
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar dados das ações: {e}")
        st.error("Erro ao carregar lista de ações. Tente novamente mais tarde.")
        return pd.DataFrame()

@lru_cache(maxsize=128)
def pegar_info_empresa(sigla_acao):
    """Obtém informações da empresa via yfinance com cache."""
    try:
        ticker = yf.Ticker(sigla_acao)
        return ticker.info, ticker
    except Exception as e:
        logging.error(f"Erro ao obter info da empresa {sigla_acao}: {e}")
        return {}, None

@lru_cache(maxsize=128)
def pegar_valores_online(sigla_acao, start_date, end_date):
    """Baixa dados históricos de ações com cache."""
    try:
        df = yf.download(sigla_acao, start=start_date, end=end_date, progress=False)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        logging.error(f"Erro ao baixar valores de {sigla_acao}: {e}")
        return pd.DataFrame()

def configurar_grafico(fig, title, x_title='Data', y_title='Valor'):
    """Configuração reutilizável para gráficos Plotly."""
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    return {'displayModeBar': False, 'scrollZoom': False}

def calcular_estocastico_lento(df, n=14):
    """Calcula o Estocástico Lento."""
    df['L14'] = df['Low'].rolling(window=n).min()
    df['H14'] = df['High'].rolling(window=n).max()
    df['%K'] = 100 * ((df['Close'] - df['L14']) / (df['H14'] - df['L14']))
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df.dropna()

def calcular_indicadores_financeiros(df):
    """Calcula indicadores financeiros adicionais."""
    df['Retorno_Diario'] = df['Close'].pct_change()
    df['Volatilidade_30d'] = df['Retorno_Diario'].rolling(window=30).std() * (252 ** 0.5)  # Anualizada
    df['RSI'] = compute_rsi(df['Close'])
    return df

def compute_rsi(close, periods=14):
    """Calcula o RSI (Relative Strength Index)."""
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def criar_grafico_dividendos(dividendos):
    """Cria gráfico de dividendos."""
    if dividendos.empty:
        st.warning("Nenhum dado de dividendos disponível.")
        return None
    fig = px.bar(dividendos, x=dividendos.index, y='Dividends', title="Evolução dos Dividendos",
                 labels={'index': 'Data', 'Dividends': 'Valor (R$)'}, color_discrete_sequence=['#1f77b4'])
    config = configurar_grafico(fig, "Evolução dos Dividendos")
    return fig

def exibir_info_empresa(info, ticker):
    """Exibe informações detalhadas da empresa."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(info.get('shortName', 'N/A'))
        st.write(f"**Nome completo:** {info.get('longName', 'N/A')}")
        st.write(f"**Setor:** {info.get('sector', 'N/A')} - **Indústria:** {info.get('industry', 'N/A')}")
        st.write(f"**Site:** {info.get('website', 'N/A')}")
        st.write(f"**Descrição:** {info.get('longBusinessSummary', 'N/A')[:500]}...")
    
    with col2:
        st.write(f"**Preço Atual:** {info.get('currentPrice', 'N/A')} {info.get('financialCurrency', 'N/A')}")
        st.write(f"**Máxima 52 Semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**Mínima 52 Semanas:** {info.get('fiftyTwoWeekLow', 'N/A')}")
        st.write(f"**Dividend Yield:** {ticker.info.get('dividendYield', 0) * 100:.2f}%")

    with st.expander("Mais Detalhes Financeiros"):
        st.write(f"**P/L Ratio:** {info.get('trailingPE', 'N/A')}")
        st.write(f"**P/VP:** {info.get('priceToBook', 'N/A')}")
        st.write(f"**ROE:** {info.get('returnOnEquity', 'N/A')}")
        st.write(f"**Dívida Líquida/EBITDA:** {info.get('debtToEquity', 'N/A')}")

# Configurações globais
DATA_INICIO_PADRAO = '2010-01-01'
DATA_FIM_PADRAO = date.today().strftime('%Y-%m-%d')

# Interface do Streamlit
try:
    logo = Image.open("logo.png")
    st.image(logo, width=250)
    st.sidebar.image(logo, width=150)
except FileNotFoundError:
    st.warning("Logo não encontrado. Certifique-se de que 'logo.png' está no diretório correto.")

st.sidebar.markdown("### Configurações")
df_acoes = pegar_dados_acoes()
if df_acoes.empty:
    st.stop()

nome_acao = st.sidebar.selectbox("Escolha uma ação:", df_acoes['snome'])
sigla_acao = df_acoes[df_acoes['snome'] == nome_acao]['sigla_acao'].iloc[0] + '.SA'

data_inicio = st.sidebar.date_input("Data Início", datetime.strptime(DATA_INICIO_PADRAO, '%Y-%m-%d'))
data_fim = st.sidebar.date_input("Data Fim", datetime.strptime(DATA_FIM_PADRAO, '%Y-%m-%d'))

# Carregar dados
info, ticker = pegar_info_empresa(sigla_acao)
df_valores = pegar_valores_online(sigla_acao, data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d'))
if df_valores.empty:
    st.error("Nenhum dado disponível para o período selecionado.")
    st.stop()

# Exibir informações
st.header(f"Análise de {nome_acao}")
exibir_info_empresa(info, ticker)

# Gráfico de preços
st.subheader("Histórico de Preços")
fig_precos = go.Figure()
fig_precos.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Close'], name='Fechamento', line_color='blue'))
fig_precos.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Open'], name='Abertura', line_color='orange'))
config = configurar_grafico(fig_precos, "Histórico de Preços", y_title="Preço (R$)")
st.plotly_chart(fig_precos, use_container_width=True, config=config)

# Médias móveis e indicadores
df_valores = calcular_indicadores_financeiros(df_valores)
fig_medias = go.Figure()
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Close'], name='Fechamento', line_color='blue'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['SMA_50'], name='SMA 50', line_color='red'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['EMA_200'], name='EMA 200', line_color='green'))
config = configurar_grafico(fig_medias, "Médias Móveis", y_title="Preço (R$)")
st.plotly_chart(fig_medias, use_container_width=True, config=config)

# Gráfico de dividendos
dividendos = ticker.dividends
if not dividendos.empty:
    fig_dividendos = criar_grafico_dividendos(dividendos)
    st.plotly_chart(fig_dividendos, use_container_width=True, config=config)

# Gráfico Estocástico e RSI
df_mensal = df_valores.resample('M', on='Date').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna()
df_mensal = calcular_estocastico_lento(df_mensal)
fig_estocastico = go.Figure()
fig_estocastico.add_trace(go.Scatter(x=df_mensal.index, y=df_mensal['%K'], name='%K', line_color='blue'))
fig_estocastico.add_trace(go.Scatter(x=df_mensal.index, y=df_mensal['%D'], name='%D', line_color='red'))
fig_estocastico.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Sobrecompra")
fig_estocastico.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Sobrevenda")
config = configurar_grafico(fig_estocastico, "Estocástico Lento (Mensal)")
st.plotly_chart(fig_estocastico, use_container_width=True, config=config)

# RSI
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['RSI'], name='RSI', line_color='purple'))
fig_rsi.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Sobrecompra")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Sobrevenda")
config = configurar_grafico(fig_rsi, "RSI (Índice de Força Relativa)")
st.plotly_chart(fig_rsi, use_container_width=True, config=config)
