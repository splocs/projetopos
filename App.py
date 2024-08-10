
import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date
import plotly.express as px

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

# Remova o decorador
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
    st.write(f"**Preço Fechamento Anterior:** {info.get('previousClose', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior Mercado Regular:** {info.get('regularMarketPreviousClose', 'N/A')}")
    st.write(f"**Preço de Compra Atual(Bid):** {info.get('bid', 'N/A')}")
    st.write(f"**Preço de Venda Atual (Ask):** {info.get('ask', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 50 dias:** {info.get('fiftyDayAverage', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 200 dias:** {info.get('twoHundredDayAverage', 'N/A')}")
    st.write(f"**Máxima das últimas 52 semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
    st.write(f"**Preço atual:** {info.get('currentPrice', 'N/A')}")
    st.write(f"**Preço/Vendas nos últimos 12 meses:** {info.get('priceToSalesTrailing12Months', 'N/A')}")

    st.markdown("#### Recomendações Analistas") 
    st.write(f"**Média das recomendações:** {info.get('recommendationMean', 'N/A')}")
    st.write(f"**Preço alvo máximo:** {info.get('targetHighPrice', 'N/A')}")
    st.write(f"**Preço alvo mínimo:** {info.get('targetLowPrice', 'N/A')}")
    st.write(f"**Preço médio alvo:** {info.get('targetMeanPrice', 'N/A')}")
    st.write(f"**Preço mediano alvo:** {info.get('targetMedianPrice', 'N/A')}")
    st.write(f"Número de opiniões de analistas: {info.get('numberOfAnalystOpinions', 'N/A')}")
    st.write(f"Recomendação: {info.get('recommendationKey', 'N/A')}")

    st.markdown("#### Volume") 
    st.write(f"**Volume médio:** {info.get('averageVolume', 'N/A')}")
    st.write(f"**Volume médio últimos 10 dias:** {info.get('averageVolume10days', 'N/A')}")

    st.markdown("#### Float") 
    st.write(f"**Ações em circulação:** {info.get('sharesOutstanding', 'N/A')}")
    st.write(f"**Free Float:** {info.get('floatShares', 'N/A')}")   
    st.write(f"**Percentual mantido por insiders:** {info.get('heldPercentInsiders', 'N/A')}")
    st.write(f"**Percentual mantido por instituições:** {info.get('heldPercentInstitutions', 'N/A')}")
    st.write(f"**Número de Ações mantidas por insiders:** {info.get('impliedSharesOutstanding', 'N/A')}")
   
    st.markdown("#### Dividendos") 
    st.write(f"**Dividendos:** {info.get('sigla_acao.dividends', 'N/A')}")
    st.write(f"**Taxa de dividendos:** {info.get('dividendRate', 'N/A')}")
    st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
    st.write(f"**Data do ex dividendos:** {info.get('exDividendDate', 'N/A')}")
    st.write(f"**Índice de pagamento:** {info.get('payoutRatio', 'N/A')}")
    st.write(f"**Rendimento médio de dividendos últimos cinco anos:** {info.get('fiveYearAvgDividendYield', 'N/A')}")

  
    # Exibindo o DataFrame de dividendos dentro de um expander
    with st.expander("Histórico de Dividendos", expanded=False):
        if not dividendos.empty:
            st.dataframe(dividendos)
            grafico = criar_grafico_dividendos(dividendos)
            st.plotly_chart(grafico)
        else:
            st.write("Nenhum dividendo encontrado.")

            

    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) em retrospecto:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) projetado:** {info.get('forwardPE', 'N/A')}")
    st.write(f"**Capitalização de mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Valor da empresa:** {info.get('enterpriseValue', 'N/A')}")
    st.write(f"**Margens de lucro:** {info.get('profitMargins', 'N/A')}")
    st.write(f"**Valor contábil:** {info.get('bookValue', 'N/A')}")
    st.write(f"**Preço/Valor contábil:** {info.get('priceToBook', 'N/A')}")
    st.write(f"**Fim do último ano fiscal:** {info.get('lastFiscalYearEnd', 'N/A')}")
    st.write(f"**Fim do próximo ano fiscal:** {info.get('nextFiscalYearEnd', 'N/A')}")
    st.write(f"**Trimestre mais recente:** {info.get('mostRecentQuarter', 'N/A')}")
    st.write(f"**Crescimento trimestral dos lucros:** {info.get('earningsQuarterlyGrowth', 'N/A')}")
    st.write(f"**Lucro líquido comum:** {info.get('netIncomeToCommon', 'N/A')}")
    st.write(f"**EPS (Lucro por ação) em retrospecto:** {info.get('trailingEps', 'N/A')}")
    st.write(f"**EPS (Lucro por ação) projetado:** {info.get('forwardEps', 'N/A')}")
    st.write(f"**Último fator de divisão:** {info.get('lastSplitFactor', 'N/A')}")
    st.write(f"**Última data de divisão:** {info.get('lastSplitDate', 'N/A')}")
    st.write(f"**IPO:** {info.get('ipoExpectedDate', 'N/A')}")
    st.write(f"**Receita trimestral:** {info.get('quarterlyRevenueGrowth', 'N/A')}")
    st.write(f"**Valor das vendas:** {info.get('revenue', 'N/A')}")
    st.write(f"**Empresa/Receita:** {info.get('enterpriseToRevenue', 'N/A')}")
    st.write(f"**Empresa/EBITDA:** {info.get('enterpriseToEbitda', 'N/A')}")
    st.write(f"**Mudança em 52 semanas:** {info.get('52WeekChange', 'N/A')}")
    st.write(f"**Mudança em 52 semanas (S&P):** {info.get('SandP52WeekChange', 'N/A')}")
    st.write(f"**Valor do último dividendo:** {info.get('lastDividendValue', 'N/A')}")
    st.write(f"**Data do último dividendo:** {info.get('lastDividendDate', 'N/A')}")
    st.write(f"**Tipo de cotação:** {info.get('quoteType', 'N/A')}")
    st.write(f"**Data da primeira negociação (UTC):** {info.get('firstTradeDateEpochUtc', 'N/A')}")
    st.write(f"Total de dinheiro: {info.get('totalCash', 'N/A')}")
    st.write(f"Total de dinheiro por ação: {info.get('totalCashPerShare', 'N/A')}")
    st.write(f"EBITDA: {info.get('ebitda', 'N/A')}")
    st.write(f"Dívida total: {info.get('totalDebt', 'N/A')}")
    st.write(f"Índice rápido: {info.get('quickRatio', 'N/A')}")
    st.write(f"Índice de liquidez corrente: {info.get('currentRatio', 'N/A')}")
    st.write(f"Receita total: {info.get('totalRevenue', 'N/A')}")
    st.write(f"Dívida/Patrimônio líquido: {info.get('debtToEquity', 'N/A')}")
    st.write(f"Receita por ação: {info.get('revenuePerShare', 'N/A')}")
    st.write(f"Retorno sobre ativos: {info.get('returnOnAssets', 'N/A')}")
    st.write(f"Retorno sobre patrimônio líquido: {info.get('returnOnEquity', 'N/A')}")
    st.write(f"Fluxo de caixa livre: {info.get('freeCashflow', 'N/A')}")
    st.write(f"Fluxo de caixa operacional: {info.get('operatingCashflow', 'N/A')}")
    st.write(f"Crescimento dos lucros: {info.get('earningsGrowth', 'N/A')}")
    st.write(f"Crescimento da receita: {info.get('revenueGrowth', 'N/A')}")
    st.write(f"Margens brutas: {info.get('grossMargins', 'N/A')}")
    st.write(f"Margens EBITDA: {info.get('ebitdaMargins', 'N/A')}")
    st.write(f"Margens operacionais: {info.get('operatingMargins', 'N/A')}")

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


    





