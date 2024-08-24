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

def criar_grafico_dividendos(dividendos):
    fig = px.bar(dividendos, x=dividendos.index, y='Dividends', title="Evolução dos Dividendos", 
                  labels={'index': '', 'Dividends': ''}, color_discrete_sequence=['blue'])
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        title_x=0.5,
        title_y=0.9,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig.show(config={
        'displayModeBar': False,
        'scrollZoom': False
    })
    return fig

def formatar_data(data):
    if data is not None:
        return pd.to_datetime(data, unit='s').strftime('%d-%m-%Y')
    return 'N/A'

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

def pegar_info_empresa(sigla_acao):
    ticker = yf.Ticker(sigla_acao)
    info = ticker.info
    return info, ticker

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

def configurar_grafico(fig):
    fig.update_layout(title='Análise de Tendência de Longo Prazo',
                   xaxis_title='Data',
                   yaxis_title='Preço',
                   xaxis_rangeslider_visible=False)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return {'displayModeBar': False, 'scrollZoom': False}

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

# Pegar os valores históricos da ação
df_valores = pegar_valores_online(sigla_acao_escolhida)

# Criando gráfico de preços
st.subheader('Gráfico de Preços')
fig = go.Figure()

fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Close'],
                         name='Preço Fechamento',
                         line_color='yellow'))

fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Open'],
                         name='Preço Abertura',
                         line_color='blue'))

config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)

# Calculando a média móvel simples (SMA) de 50 dias e 200 dias
df_valores['SMA_50'] = df_valores['Close'].rolling(window=50).mean()
df_valores['SMA_200'] = df_valores['Close'].rolling(window=200).mean()

# Calculando a média móvel exponencial (EMA) de 50 dias e 200 dias
df_valores['EMA_50'] = df_valores['Close'].ewm(span=50, adjust=False).mean()
df_valores['EMA_200'] = df_valores['Close'].ewm(span=200, adjust=False).mean()

# Criando o gráfico de preços com as médias móveis
fig = go.Figure()

# Adicionando os preços de fechamento
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Close'],
                         name='Preço Fechamento',
                         line_color='blue'))

# Adicionando as médias móveis simples
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['SMA_50'],
                         name='SMA 50 (Tendência de curto prazo)',
                         line_color='red'))

fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['SMA_200'],
                         name='SMA 200 (Tendência de longo prazo)',
                         line_color='green'))

# Adicionando as médias móveis exponenciais
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['EMA_50'],
                         name='EMA 50 (Tendência de curto prazo)',
                         line_color='purple'))

fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['EMA_200'],
                         name='EMA 200 (Tendência de longo prazo)',
                         line_color='orange'))

# Configurando layout do gráfico
fig.update_layout(title='Análise de Tendência de Longo Prazo',
                   xaxis_title='Data',
                   yaxis_title='Preço',
                   xaxis_rangeslider_visible=False)

# Exibindo o gráfico no Streamlit
config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)


    





