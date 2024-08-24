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

def configurar_grafico(fig):
    fig.update_layout(
        showlegend=True,
        xaxis_title=None,
        yaxis_title=None,
        title_x=0.5,
        title_y=0.9,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    return {'displayModeBar': False, 'scrollZoom': False}

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

# Criando gráfico de preços de fechamento e abertura
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

# Adicionando expander com vídeo explicativo para Preço de Fechamento e Abertura
with st.expander("Clique para assistir ao vídeo explicativo sobre Preço de Fechamento e Abertura", expanded=False):
    st.video("https://www.youtube.com/watch?v=sdhO_eKyA-0")

# Calculando as médias móveis simples (SMA) de 50 dias e 200 dias
df_valores['SMA_50'] = df_valores['Close'].rolling(window=50).mean()
df_valores['SMA_200'] = df_valores['Close'].rolling(window=200).mean()

# Calculando as médias móveis exponenciais (EMA) de 50 dias e 200 dias
df_valores['EMA_50'] = df_valores['Close'].ewm(span=50, adjust=False).mean()
df_valores['EMA_200'] = df_valores['Close'].ewm(span=200, adjust=False).mean()

# Criando o gráfico de preços com as médias móveis
st.subheader('Gráfico com Médias Móveis')
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

config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)



# Determinando a tendência com base nas médias móveis
tendencia = None
if df_valores['Close'].iloc[-1] > df_valores['SMA_50'].iloc[-1] and df_valores['Close'].iloc[-1] > df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de alta'
    explicacao_tendencia = "O preço de fechamento está acima das médias móveis de curto e longo prazo, sugerindo uma tendência de alta consistente."
elif df_valores['Close'].iloc[-1] < df_valores['SMA_50'].iloc[-1] and df_valores['Close'].iloc[-1] < df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de baixa'
    explicacao_tendencia = "O preço de fechamento está abaixo das médias móveis de curto e longo prazo, indicando uma tendência de baixa persistente."
elif df_valores['Close'].iloc[-1] > df_valores['SMA_50'].iloc[-1] and df_valores['Close'].iloc[-1] < df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de alta em formação'
    explicacao_tendencia = "O preço de fechamento está acima da média móvel de curto prazo, mas abaixo da média móvel de longo prazo, sugerindo uma possível tendência de alta em desenvolvimento."
elif df_valores['Close'].iloc[-1] < df_valores['SMA_50'].iloc[-1] and df_valores['Close'].iloc[-1] > df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de baixa em formação'
    explicacao_tendencia = "O preço de fechamento está abaixo da média móvel de curto prazo, mas acima da média móvel de longo prazo, indicando uma possível tendência de baixa em desenvolvimento."
else:
    tendencia = 'Estabilização ou acumulação'
    explicacao_tendencia = "O preço de fechamento está entre as médias móveis de curto e longo prazo, sugerindo um período de estabilização ou acumulação no mercado."

# Exibindo mensagem com a tendência e explicação
st.markdown(f"A ação está atualmente em **{tendencia}**. {explicacao_tendencia}")

# Adicionando expander com vídeo explicativo para Médias Móveis
with st.expander("Clique para assistir ao vídeo explicativo sobre Médias Móveis", expanded=False):
    st.video("https://www.youtube.com/watch?v=uPAqMymYYGs")
    
# Convertendo os dados para frequência mensal
df_valores_mensal = df_valores.resample('M', on='Date').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
}).dropna()

# Calculando o Estocástico Lento
df_valores_mensal = calcular_estocastico_lento(df_valores_mensal)

# Criando gráfico do Estocástico Lento
st.subheader('Gráfico Estocástico Lento (Mensal)')
fig = go.Figure()

# %K
fig.add_trace(go.Scatter(x=df_valores_mensal.index,
                         y=df_valores_mensal['%K'],
                         name='%K',
                         line_color='blue'))

# %D
fig.add_trace(go.Scatter(x=df_valores_mensal.index,
                         y=df_valores_mensal['%D'],
                         name='%D',
                         line_color='red'))

# Linha de sobrecompra e sobrevenda
fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Sobrecompra", annotation_position="top left")
fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Sobrevenda", annotation_position="bottom left")

# Configurando layout do gráfico
fig.update_layout(title='Estocástico Lento (Mensal)',
                   xaxis_title='Data',
                   yaxis_title='Valor',
                   xaxis_rangeslider_visible=False)

config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)

# Adicionando expander com vídeo explicativo para Estocástico Lento (a ser adicionado, se necessário)
with st.expander("Clique para assistir ao vídeo explicativo sobre Estocástico Lento", expanded=False):
    st.video("https://www.youtube.com/watch?v=exemplo_video_estocastico_lento")  # Substitua com o link do vídeo apropriado





