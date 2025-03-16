import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Configurando a largura da página
st.set_page_config(
    page_title="Plotos.com.br",
    page_icon="FAV.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def configurar_grafico(fig, title, x_title="Data", y_title="Valor"):
    """Configurações padrão para todos os gráficos."""
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

def criar_grafico_dividendos(dividendos):
    """Cria gráfico de dividendos corrigido para Streamlit."""
    if dividendos.empty:
        st.warning("Nenhum dado de dividendos disponível.")
        return None
    fig = px.bar(dividendos, x=dividendos.index, y='Dividends', title="Evolução dos Dividendos",
                 labels={'index': 'Data', 'Dividends': 'Valor (R$)'}, color_discrete_sequence=['#1f77b4'])
    config = configurar_grafico(fig, "Evolução dos Dividendos")
    return fig

def pegar_dados_acoes():
    """Carrega lista de ações com tratamento de erro."""
    try:
        path = 'https://raw.githubusercontent.com/splocs/meu-repositorio/main/acoes.csv'
        return pd.read_csv(path, delimiter=';')
    except Exception as e:
        st.error(f"Erro ao carregar lista de ações: {e}")
        return pd.DataFrame()

def pegar_valores_online(sigla_acao):
    """Baixa dados históricos com tratamento de erro."""
    try:
        df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM, progress=False)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro ao baixar dados da ação {sigla_acao}: {e}")
        return pd.DataFrame()

def calcular_estocastico_lento(df, n=14):
    """Calcula o Estocástico Lento."""
    df['L14'] = df['Low'].rolling(window=n).min()
    df['H14'] = df['High'].rolling(window=n).max()
    df['%K'] = 100 * ((df['Close'] - df['L14']) / (df['H14'] - df['L14']))
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df.dropna()

def pegar_info_empresa(sigla_acao):
    """Obtém informações da empresa com tratamento de erro."""
    try:
        ticker = yf.Ticker(sigla_acao)
        info = ticker.info
        return info, ticker
    except Exception as e:
        st.error(f"Erro ao carregar informações da empresa {sigla_acao}: {e}")
        return {}, None

def exibir_info_empresa(info, dividendos):
    """Exibe informações da empresa."""
    st.write(f"{info.get('shortName', 'N/A')}")
    st.write(f"**Nome completo:** {info.get('longName', 'N/A')}")
    st.write(f"**Endereço:** {info.get('address1', 'N/A')}")
    st.write(f"**Cidade:** {info.get('city', 'N/A')}")
    st.write(f"**Estado:** {info.get('state', 'N/A')}")
    st.write(f"**País:** {info.get('country', 'N/A')}")
    st.write(f"**CEP:** {info.get('zip', 'N/A')}")
    st.write(f"**Telefone:** {info.get('phone', 'N/A')}")
    st.write(f"**Site:** {info.get('website', 'N/A')}")
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
    st.write(f"Moeda financeira: {info.get('financialCurrency', 'N/A')}")
    st.write(f"**Descrição:** {info.get('longBusinessSummary', 'N/A')}")
    
    with st.expander("Diretores da Empresa", expanded=False):
        directors = info.get('companyOfficers', [])
        if directors:
            for director in directors:
                st.write(f"- **Nome:** {director.get('name', 'N/A')}")
                st.write(f"  **Cargo:** {director.get('title', 'N/A')}")
                st.write(f"  **Idade:** {director.get('age', 'N/A')}")
                st.write(f"  **Ano de Nascimento:** {director.get('yearBorn', 'N/A')}")
        else:
            st.write("Nenhum diretor encontrado.")

    st.markdown("#### Análise de Preço")
    with st.expander("Clique para assistir ao vídeo explicativo", expanded=False):
        st.video("https://www.youtube.com/watch?v=M1KWn0vFxeo")
    
    st.write(f"**Preço atual:** {info.get('currentPrice', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior:** {info.get('previousClose', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior Mercado Regular:** {info.get('regularMarketPreviousClose', 'N/A')}")
    st.write(f"**Preço de Compra Atual(Bid):** {info.get('bid', 'N/A')}")
    st.write(f"**Preço de Venda Atual (Ask):** {info.get('ask', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 50 dias:** {info.get('fiftyDayAverage', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 200 dias:** {info.get('twoHundredDayAverage', 'N/A')}")
    st.write(f"**Máxima das últimas 52 semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')}")

# Definindo datas padrão
DATA_INICIO = '2010-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

# Carregar e exibir logo
try:
    logo = Image.open("logo.png")
    st.image(logo, width=250)
    st.sidebar.image(logo, width=150)
except FileNotFoundError:
    st.warning("Logo não encontrado. Certifique-se de que 'logo.png' está no diretório correto.")

# Sidebar
st.sidebar.markdown('Escolha a ação')
df = pegar_dados_acoes()
if df.empty:
    st.stop()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao'] + '.SA'

# Carregar dados da empresa
info_acao, ticker = pegar_info_empresa(sigla_acao_escolhida)
st.header(f"Informações da ação: {nome_acao_escolhida}")
exibir_info_empresa(info_acao, ticker.dividends)

# Carregar valores históricos
df_valores = pegar_valores_online(sigla_acao_escolhida)
if df_valores.empty or len(df_valores) < 200:
    st.error("Dados insuficientes para análise. Tente outra ação ou período.")
    st.stop()

# Gráfico de Abertura e Fechamento
st.subheader('Gráfico de Abertura e Fechamento')
fig_precos = go.Figure()
fig_precos.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Close'], name='Fechamento', line_color='yellow'))
fig_precos.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Open'], name='Abertura', line_color='blue'))
config = configurar_grafico(fig_precos, "Preços de Abertura e Fechamento", y_title="Preço (R$)")
st.plotly_chart(fig_precos, use_container_width=True, config=config)

with st.expander("Clique para assistir ao vídeo explicativo sobre Preço de Fechamento e Abertura", expanded=False):
    st.video("https://www.youtube.com/watch?v=z59Rf9xNpFY")

# Médias Móveis
df_valores['SMA_50'] = df_valores['Close'].rolling(window=50).mean()
df_valores['SMA_200'] = df_valores['Close'].rolling(window=200).mean()
df_valores['EMA_50'] = df_valores['Close'].ewm(span=50, adjust=False).mean()
df_valores['EMA_200'] = df_valores['Close'].ewm(span=200, adjust=False).mean()

st.subheader('Gráfico com Médias Móveis')
fig_medias = go.Figure()
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Close'], name='Fechamento', line_color='blue'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['SMA_50'], name='SMA 50', line_color='red'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['SMA_200'], name='SMA 200', line_color='green'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['EMA_50'], name='EMA 50', line_color='purple'))
fig_medias.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['EMA_200'], name='EMA 200', line_color='orange'))
config = configurar_grafico(fig_medias, "Análise de Tendência com Médias Móveis", y_title="Preço (R$)")
st.plotly_chart(fig_medias, use_container_width=True, config=config)

# Tendência (com lógica robusta)
tendencia = "Dados insuficientes para determinar tendência"
explicacao_tendencia = "Não há dados suficientes ou as médias móveis ainda não foram calculadas para o período."
if len(df_valores) >= 200:
    ultimo_close = df_valores['Close'].iloc[-1]
    ultimo_sma_50 = df_valores['SMA_50'].iloc[-1]
    ultimo_sma_200 = df_valores['SMA_200'].iloc[-1]
    
    if pd.notna(ultimo_close) and pd.notna(ultimo_sma_50) and pd.notna(ultimo_sma_200):
        if ultimo_close > ultimo_sma_50 and ultimo_close > ultimo_sma_200:
            tendencia = 'Tendência de alta'
            explicacao_tendencia = "O preço de fechamento está acima das médias móveis de curto e longo prazo, sugerindo uma tendência de alta consistente."
        elif ultimo_close < ultimo_sma_50 and ultimo_close < ultimo_sma_200:
            tendencia = 'Tendência de baixa'
            explicacao_tendencia = "O preço de fechamento está abaixo das médias móveis de curto e longo prazo, indicando uma tendência de baixa persistente."
        elif ultimo_close > ultimo_sma_50 and ultimo_close < ultimo_sma_200:
            tendencia = 'Tendência de alta em formação'
            explicacao_tendencia = "O preço de fechamento está acima da média móvel de curto prazo, mas abaixo da média móvel de longo prazo, sugerindo uma possível tendência de alta em desenvolvimento."
        elif ultimo_close < ultimo_sma_50 and ultimo_close > ultimo_sma_200:
            tendencia = 'Tendência de baixa em formação'
            explicacao_tendencia = "O preço de fechamento está abaixo da média móvel de curto prazo, mas acima da média móvel de longo prazo, indicando uma possível tendência de baixa em desenvolvimento."
        else:
            tendencia = 'Estabilização ou acumulação'
            explicacao_tendencia = "O preço de fechamento está entre as médias móveis de curto e longo prazo, sugerindo um período de estabilização ou acumulação no mercado."

st.markdown(f"A ação está atualmente em **{tendencia}**. {explicacao_tendencia}")
with st.expander("Clique para assistir ao vídeo explicativo sobre Médias Móveis", expanded=False):
    st.video("https://www.youtube.com/watch?v=dUdYE2aIS00")

# Estocástico Lento
df_valores_mensal = df_valores.resample('M', on='Date').agg({
    'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'
}).dropna()
df_valores_mensal = calcular_estocastico_lento(df_valores_mensal)

st.subheader('Gráfico Estocástico Lento (Mensal)')
fig_estocastico = go.Figure()
fig_estocastico.add_trace(go.Scatter(x=df_valores_mensal.index, y=df_valores_mensal['%K'], name='%K', line_color='blue'))
fig_estocastico.add_trace(go.Scatter(x=df_valores_mensal.index, y=df_valores_mensal['%D'], name='%D', line_color='red'))
fig_estocastico.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Sobrecompra")
fig_estocastico.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Sobrevenda")
config = configurar_grafico(fig_estocastico, "Estocástico Lento (Mensal)")
st.plotly_chart(fig_estocastico, use_container_width=True, config=config)

with st.expander("Clique para assistir ao vídeo explicativo sobre Estocástico Lento", expanded=False):
    st.video("https://www.youtube.com/watch?v=oKm1zi85PYE")

# Gráfico de Dividendos
dividendos = ticker.dividends
if not dividendos.empty:
    fig_dividendos = criar_grafico_dividendos(dividendos)
    if fig_dividendos:
        st.plotly_chart(fig_dividendos, use_container_width=True, config=config)
