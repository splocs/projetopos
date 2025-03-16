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
    fig.show(config={'displayModeBar': False, 'scrollZoom': False})
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

def calcular_estocastico_lento(df, n=14):
    df['L14'] = df['Low'].rolling(window=n).min()
    df['H14'] = df['High'].rolling(window=n).max()
    df['%K'] = 100 * ((df['Close'] - df['L14']) / (df['H14'] - df['L14']))
    df['%D'] = df['%K'].rolling(window=3).mean()
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
    
    # Calculando Estocástico Lento
    df_valores_mensal = pegar_valores_online(info.get('symbol', 'N/A'))
    df_valores_mensal = calcular_estocastico_lento(df_valores_mensal)
    fig = go.Figure()

    # Plotando %K
    fig.add_trace(go.Scatter(x=df_valores_mensal.index,
                             y=df_valores_mensal['%K'],
                             name='%K',
                             line_color='blue'))

    # Plotando %D
    fig.add_trace(go.Scatter(x=df_valores_mensal.index,
                             y=df_valores_mensal['%D'],
                             name='%D',
                             line_color='red'))

    # Configurar gráfico
    fig.update_layout(title='Estocástico Lento - Análise Mensal',
                      xaxis_title='Data',
                      yaxis_title='Valor',
                      xaxis_rangeslider_visible=False)

    # Exibir o gráfico
    config = configurar_grafico(fig)
    st.plotly_chart(fig, use_container_width=False, config=config)

    # Adicionando expander com vídeo explicativo para Estocástico Lento
    with st.expander("Clique para assistir ao vídeo explicativo sobre Estocástico Lento", expanded=False):
        st.video("https://www.youtube.com/watch?v=nMjpO1djlIo")

    # Exibindo a tabela de dividendos mensais
    st.subheader('Dividendos Mensais')
    dividendos_mensais = dividendos.resample('M').sum()
    st.write(dividendos_mensais)

    # Adicionando expander com vídeo explicativo sobre Dividendos
    with st.expander("Clique para assistir ao vídeo explicativo sobre Dividendos", expanded=False):
        st.video("https://www.youtube.com/watch?v=1EJz2LOjY0k")

    # Finalização do aplicativo
    st.markdown("### Análise Concluída")
    st.write("Este aplicativo oferece uma análise detalhada de ações, com gráficos de preço, médias móveis, estocástico lento e dividendos, além de vídeos explicativos para melhor compreensão de cada indicador e tendência.")
    st.write("Agradecemos por utilizar o Plotos.com.br para suas análises de mercado!")

    # Finalizando a sidebar
    st.sidebar.markdown('### Mais Informações')
    st.sidebar.markdown('Para mais informações sobre o mercado financeiro, visite [Plotos.com.br](http://www.plotos.com.br).')
