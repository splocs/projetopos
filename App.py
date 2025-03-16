import streamlit as st
import pandas as pd
from bcb import sgs
import plotly.express as px
from datetime import date

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Taxa Selic - Histórico e Atual",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título do aplicativo
st.title("Taxa Selic - Histórico e Atual")

# Sidebar para configurações
st.sidebar.markdown("### Configurações")
data_inicio = st.sidebar.date_input("Data de Início", value=pd.to_datetime("2010-01-01"))
data_fim = st.sidebar.date_input("Data de Fim", value=date.today())

# Função para carregar os dados da Selic
@st.cache_data  # Cache para melhorar a performance
def carregar_dados_selic(start_date, end_date):
    try:
        selic = sgs.get({'Selic': 432}, start=start_date, end=end_date)
        selic = selic.rename(columns={'Selic': 'Taxa Selic (%)'})  # Renomear para clareza
        return selic
    except Exception as e:
        st.error(f"Erro ao carregar os dados da Selic: {e}")
        return pd.DataFrame()

# Carregar os dados
df_selic = carregar_dados_selic(data_inicio, data_fim)

# Verificar se os dados foram carregados
if df_selic.empty:
    st.warning("Nenhum dado disponível para o período selecionado.")
    st.stop()

# Exibir a taxa Selic atual (último valor)
ultima_taxa = df_selic['Taxa Selic (%)'].iloc[-1]
ultima_data = df_selic.index[-1].strftime('%d/%m/%Y')
st.subheader(f"Taxa Selic Atual: {ultima_taxa:.2f}%")
st.write(f"Data: {ultima_data}")

# Gráfico histórico da Selic
st.subheader("Histórico da Taxa Selic")
fig = px.line(df_selic, x=df_selic.index, y='Taxa Selic (%)', 
              title="Evolução da Taxa Selic",
              labels={'x': 'Data', 'Taxa Selic (%)': 'Taxa (%)'})
fig.update_layout(
    template="plotly_white",
    xaxis_title="Data",
    yaxis_title="Taxa Selic (%)",
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Exibir a tabela de dados (opcional, com expander)
with st.expander("Ver Tabela de Dados Históricos"):
    st.dataframe(df_selic.style.format({"Taxa Selic (%)": "{:.2f}"}), height=300)

# Rodapé
st.markdown("Fonte: Banco Central do Brasil (SGS - Sistema Gerenciador de Séries Temporais)")
