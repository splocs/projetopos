import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

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

def criar_grafico_dividendos(dividendos):
    fig = px.bar(dividendos, x=dividendos.index, y='Dividends', title="Evolução dos Dividendos", 
                  labels={'index': '', 'Dividends': ''}, color_discrete_sequence=['blue'])
    fig.update_layout(
        showlegend=False,  # Remove a legenda
        xaxis_title=None,  # Remove o título do eixo x
        yaxis_title=None,  # Remove o título do eixo y
        title_x=0.5,  # Centraliza o título
        title_y=0.9,  # Ajusta a posição do título no eixo y
        margin=dict(l=20, r=20, t=50, b=20),  # Ajusta as margens
        xaxis=dict(fixedrange=True),  # Desabilita o zoom no eixo x
        yaxis=dict(fixedrange=True)  # Desabilita o zoom no eixo y
    )
    
    # Remove o menu do Plotly
    fig.show(config={
        'displayModeBar': False,  # Remove o menu do Plotly
        'scrollZoom': False  # Desabilita o zoom com o scroll
    })

    return fig

# Função para formatar a data
def formatar_data(data):
    if data is not None:
        return pd.to_datetime(data, unit='s').strftime('%d-%m-%Y')
    return 'N/A'

# Função para pegar os dados das ações
def pegar_dados_acoes():
    path = 'https://raw.githubusercontent.com/splocs/meu-repositorio/main/acoes.csv'
    return pd.read_csv(path, delimiter=';')

def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM, progress=False)
    df.reset_index(inplace=True)
    return df

def pegar_valores_online_periodo_definido(sigla_acao, data_inicio, data_fim):
    df = yf.download(sigla_acao, data_inicio, data_fim, progress=False)
    df.reset_index(inplace=True)
    return df

# Função para pegar as informações da empresa
def pegar_info_empresa(sigla_acao):
    ticker = yf.Ticker(sigla_acao)
    info = ticker.info
    return info, ticker

# Função para exibir informações da empresa
def exibir_info_empresa(info, dividendos):
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
    
    # Exibição dos diretores dentro de um expander sem borda
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

    st.markdown("#### Preço")  
   
    # Colocar o vídeo dentro de um expander
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

    # Adição dos indicadores técnicos
    st.header("Indicadores Técnicos")

    # Pegar os valores online
    df = pegar_valores_online(sigla_acao_escolhida)
    
    # Função para calcular indicadores técnicos
    def calcular_indicadores(df):
        df['MA7'] = df['Close'].rolling(window=7).mean()
        df['MA21'] = df['Close'].rolling(window=21).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().apply(lambda x: np.nan if x == 0 else x).rolling(window=14).mean()))
        df['L14'] = df['Low'].rolling(window=14).min()
        df['H14'] = df['High'].rolling(window=14).max()
        df['%K'] = 100 * ((df['Close'] - df['L14']) / (df['H14'] - df['L14']))
        df['%D'] = df['%K'].rolling(window=3).mean()
        df['Bol_lower'] = df['Close'].rolling(window=20).mean() - 2 * df['Close'].rolling(window=20).std()
        df['Bol_upper'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()
        df['Trix'] = 100 * pd.Series(df['Close'].ewm(span=15, adjust=False).mean().diff()).ewm(span=15, adjust=False).mean().diff().ewm(span=15, adjust=False).mean() / df['Close'].ewm(span=15, adjust=False).mean().shift(1)
        return df
    
    df = calcular_indicadores(df)

    # Função para criar os gráficos
    def criar_grafico(df, tipo_grafico):
        if tipo_grafico == 'Cruzamento de Médias Móveis':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Preço Fechamento'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MA7'], mode='lines', name='MA7'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MA21'], mode='lines', name='MA21'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MA200'], mode='lines', name='MA200'))
            fig.update_layout(title='Cruzamento de Médias Móveis')
        
        elif tipo_grafico == 'Índice de Força Relativa (RSI)':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI'))
            fig.update_layout(title='Índice de Força Relativa (RSI)')

        elif tipo_grafico == 'Estocástico Lento':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['%K'], mode='lines', name='%K'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['%D'], mode='lines', name='%D'))
            fig.update_layout(title='Estocástico Lento')

        elif tipo_grafico == 'Bandas de Bollinger':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Preço Fechamento'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Bol_upper'], mode='lines', name='Bol_upper'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Bol_lower'], mode='lines', name='Bol_lower'))
            fig.update_layout(title='Bandas de Bollinger')
        
        elif tipo_grafico == 'TRIX':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Trix'], mode='lines', name='TRIX'))
            fig.update_layout(title='TRIX')

        return fig

    # Criar expanders para cada gráfico
    with st.expander("Cruzamento de Médias Móveis"):
        st.plotly_chart(criar_grafico(df, 'Cruzamento de Médias Móveis'))

    with st.expander("Índice de Força Relativa (RSI)"):
        st.plotly_chart(criar_grafico(df, 'Índice de Força Relativa (RSI)'))

    with st.expander("Estocástico Lento"):
        st.plotly_chart(criar_grafico(df, 'Estocástico Lento'))

    with st.expander("Bandas de Bollinger"):
        st.plotly_chart(criar_grafico(df, 'Bandas de Bollinger'))

    with st.expander("TRIX"):
        st.plotly_chart(criar_grafico(df, 'TRIX'))


# Definindo data de início e fim
DATA_INICIO = '2010-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

# Logo
logo_path = "logo.png"
logo = Image.open(logo_path)

# Exibir o logo no aplicativo Streamlit
st.image(logo, width=250)

# Exibir o logo na sidebar
st.sidebar.image(logo, width=150)

# Criando a sidebar
st.sidebar.markdown('Escolha a ação')

# Pegando os dados das ações
df = pegar_dados_acoes()
acao = df['snome']

nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao']
sigla_acao_escolhida += '.SA'

# Pegar e exibir as informações da empresa
info_acao, ticker = pegar_info_empresa(sigla_acao_escolhida)
st.header(f"Informações da ação: {nome_acao_escolhida}")

# Pegar e exibir o histórico de dividendos
dividendos = ticker.dividends

# Exibir as informações da empresa e o histórico de dividendos
exibir_info_empresa(info_acao, dividendos)


    





