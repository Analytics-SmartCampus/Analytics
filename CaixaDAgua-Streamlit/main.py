import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def exibicao():

    st.title('Exibição de Dados')

    st.markdown('- - -')

    # Parâmetros da simulação
    intervalo_minutos = st.selectbox('Selecione o intervalo de tempo(min)', [15, 30])
    num_dias = st.slider('Selecione o número de dias', min_value=1, max_value=7)

    st.markdown('- - -')

    st.header('Pressão de Entrada/Saída - Poço Artesiano')

    pressao_entrada_inicial = 8  # Pressão inicial de entrada em bar
    pressao_saida_inicial = 8  # Pressão inicial de saída em bar
    variacao_pressao = 0.1  # Variação máxima de pressão por intervalo em bar

    # Limites máximos e mínimos de pressão
    pressao_maxima = 10
    pressao_minima = 7

    # Calcular o número total de pontos de dados por dia
    num_pontos_por_hora = 60 // intervalo_minutos
    num_pontos_por_dia = 24 * num_pontos_por_hora

    # Gerar os tempos
    tempos = pd.date_range(start='2024-01-01 00:00:00', periods=num_pontos_por_dia * num_dias, freq=f'{intervalo_minutos}T')

    # Gerar os dados de pressão de entrada e saída
    np.random.seed(42)  # Para reprodutibilidade
    variacoes_entrada = np.random.uniform(-variacao_pressao, variacao_pressao, size=num_pontos_por_dia * num_dias)
    variacoes_saida = np.random.uniform(-variacao_pressao, variacao_pressao, size=num_pontos_por_dia * num_dias)

    # Calcular as pressões acumuladas com reset diário e limites aplicados
    pressao_entrada = []
    pressao_saida = []
    for dia in range(num_dias):
        entrada_diaria = pressao_entrada_inicial + np.cumsum(variacoes_entrada[dia * num_pontos_por_dia:(dia + 1) * num_pontos_por_dia])
        saida_diaria = pressao_saida_inicial + np.cumsum(variacoes_saida[dia * num_pontos_por_dia:(dia + 1) * num_pontos_por_dia])
        
        # Aplicar limites
        entrada_diaria = np.clip(entrada_diaria, pressao_minima, pressao_maxima)
        saida_diaria = np.clip(saida_diaria, pressao_minima, pressao_maxima)
        
        pressao_entrada.extend(entrada_diaria)
        pressao_saida.extend(saida_diaria)

    # Criar o DataFrame
    dados_pressao = pd.DataFrame({'Tempo': tempos, 'Pressao_entrada_bar': pressao_entrada, 'Pressao_saida_bar': pressao_saida})

    # Lista para armazenar os alertas
    alertas = []

    # Verificar se há pressão igual ou menor a 7 bar e emitir alerta para cada ocorrência
    for index, row in dados_pressao.iterrows():
        if row['Pressao_entrada_bar'] <= 7 or row['Pressao_saida_bar'] <= 7:
            alertas.append(f'Atenção: A pressão atingiu 7 bar ou menos no tempo {row["Tempo"]}')

    # Botão para mostrar todos os alertas
    if st.button("Mostrar Todos os Alertas"):
        for alerta in alertas:
            st.warning(alerta)

    # Botão para mostrar apenas o último alerta por padrão
    if st.button("Mostrar Último Alerta", key="ultimo_alerta"):
        if alertas:
            st.warning(alertas[-1])
        else:
            st.write("Nenhum alerta gerado ainda.")

    # Função para destacar pontos específicos
    def plot_with_highlight(ax, x, y, threshold, color='red', label=None):
        ax.plot(x, y, linestyle='-', color='green', label='Pressão')
        highlight = y <= threshold
        ax.scatter(x[highlight], y[highlight], color=color, label=label if label else f'<= {threshold} bar')

    def plot_with_highlight2(ax, x, y, threshold, color='red', label=None):
        ax.plot(x, y, linestyle='-', color='orange', label='Pressão')
        highlight = y <= threshold
        ax.scatter(x[highlight], y[highlight], color=color, label=label if label else f'<= {threshold} bar')

    # Plotar o gráfico de pressão de entrada
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    plot_with_highlight(ax1, dados_pressao['Tempo'], dados_pressao['Pressao_entrada_bar'], 7, color='red', label='<= 7 bar')
    ax1.set_xlabel('Tempo')
    ax1.set_ylabel('Pressão de Entrada (bar)')
    ax1.set_title('Pressão de Entrada no Poço Artesiano a Cada Intervalo')
    ax1.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax1.legend()

    # Plotar o gráfico de pressão de saída
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    plot_with_highlight2(ax2, dados_pressao['Tempo'], dados_pressao['Pressao_saida_bar'], 7, color='red', label='<= 7 bar')
    ax2.set_xlabel('Tempo')
    ax2.set_ylabel('Pressão de Saída (bar)')
    ax2.set_title('Pressão de Saída no Poço Artesiano a Cada Intervalo')
    ax2.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax2.legend()

    # Mostrar os gráficos no Streamlit
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Exibir os dados
    st.write(dados_pressao)

    st.markdown('- - -')

    st.header('Nível de Água(Tanque) e Volume(Hidrômetro)')

    # Parâmetros da simulação
    volume_inicial = 250000  # Volume inicial em litros
    entrada_maxima = 5000  # Consumo máximo de água por intervalo em litros
    vazao_maxima = 3500  # Vazão máxima de saída de água por intervalo em litros
    limite_maximo = 400000  # Limite máximo do volume em litros
    limite_minimo = 0  # Limite mínimo do volume em litros

    # Gerar os dados de consumo de água
    consumos = np.random.randint(0, entrada_maxima + 1, size=num_pontos_por_dia * num_dias)
    vazoes = np.random.randint(0, vazao_maxima + 1, size=num_pontos_por_dia * num_dias)

    # Calcular o volume total sem reset diário e aplicar limites
    volumes = []
    volume_atual = volume_inicial
    for consumo, vazao in zip(consumos, vazoes):
        volume_atual = np.clip(volume_atual + consumo - vazao, limite_minimo, limite_maximo)
        volumes.append(volume_atual)

    # Criar o DataFrame
    dados_volume = pd.DataFrame({'Tempo': tempos, 'Volume_total_L': volumes})

    # Calcular a altura da água na caixa d'água
    raio = 2.5  # raio em metros
    area_base = np.pi * raio ** 2  # área da base do cilindro em metros quadrados
    dados_volume['Nivel_agua_mm'] = (dados_volume['Volume_total_L'] / 1000) / area_base * 1000

    # Variáveis para armazenar os últimos alertas de 100.000 e 400.000 litros
    ultimo_alerta_100k = None
    ultimo_alerta_400k = None

    # Verificar volumes específicos e emitir alertas
    volume_100k = dados_volume[dados_volume['Volume_total_L'] <= 100000]
    volume_400k = dados_volume[dados_volume['Volume_total_L'] == 400000]

    if not volume_100k.empty:
        for _, row in volume_100k.iterrows():
            ultimo_alerta_100k = f'Atenção: O volume atingiu valores menores que 100.000 litros no tempo {row["Tempo"]}!'

    if not volume_400k.empty:
        for _, row in volume_400k.iterrows():
            ultimo_alerta_400k = f'Atenção: O volume atingiu seu limite máximo no tempo {row["Tempo"]}!'

    # Botão para mostrar apenas o último alerta de 100.000 litros
    if st.button("Mostrar Último Alerta de 100.000 Litros", key="ultimo_alerta_100k"):
        if ultimo_alerta_100k:
            st.warning(ultimo_alerta_100k)
        else:
            st.write("Nenhum alerta de 100.000 litros gerado ainda.")

    # Botão para mostrar apenas o último alerta de 400.000 litros
    if st.button("Mostrar Último Alerta de 400.000 Litros", key="ultimo_alerta_400k"):
        if ultimo_alerta_400k:
            st.warning(ultimo_alerta_400k)
        else:
            st.write("Nenhum alerta de 400.000 litros gerado ainda.")

    def plot_with_highlight_combined(ax, x, y, highlight_points_100k, highlight_points_400k, color_100k='red', color_400k='pink', label_100k='100.000 L', label_400k='400.000 L'):
        ax.plot(x, y, linestyle='-', color='blue', label='Volume')
        if not highlight_points_100k.empty:
            ax.scatter(highlight_points_100k['Tempo'], highlight_points_100k['Volume_total_L'], color=color_100k, label=label_100k)
        if not highlight_points_400k.empty:
            ax.scatter(highlight_points_400k['Tempo'], highlight_points_400k['Volume_total_L'], color=color_400k, label=label_400k)


    # Plotar o gráfico de nível de água
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(dados_volume['Tempo'], dados_volume['Nivel_agua_mm'], linestyle='-', color='purple')
    ax3.set_xlabel('Tempo')
    ax3.set_ylabel('Nível de Água (mm)')
    ax3.set_title('Nível de Água do Tanque')
    ax3.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Plotar o gráfico de volume total com destaques combinados
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    plot_with_highlight_combined(ax4, dados_volume['Tempo'], dados_volume['Volume_total_L'], volume_100k, volume_400k)
    ax4.set_xlabel('Tempo')
    ax4.set_ylabel('Volume Total (L)')
    ax4.set_title('Volume Total no Hidrômetro')
    ax4.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax4.legend()

    # Exibir os gráficos no Streamlit
    st.pyplot(fig3)
    st.pyplot(fig4)

    # Exibir os dados no Streamlit
    st.write(dados_volume)

    return dados_pressao, dados_volume

def analise(dados_pressao, dados_volume):
    st.title('Análise de Dados')

    st.markdown('- - -')

    descricaoVol = dados_volume.describe()
    descricaoPres  = dados_pressao.describe()

    descricaoVol = descricaoVol.rename(index={
    'count': 'Pontos',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Mínimo',
    '25%': '25%',
    '50%': 'Mediana',
    '75%': '75%',
    'max': 'Máximo'
    })

    descricaoPres = descricaoPres.rename(index={
    'count': 'Pontos',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Mínimo',
    '25%': '25%',
    '50%': 'Mediana',
    '75%': '75%',
    'max': 'Máximo'
    })

    # Resumo Estatístico
    st.header('Resumo Estatístico')
    st.subheader('Pressão')
    st.write(descricaoPres)

    st.subheader('Volume de Água')
    st.write(descricaoVol)

    st.markdown('- - -')

    # Correlação
    dados_completos = pd.merge(dados_pressao, dados_volume, on='Tempo')

    # Tendências Temporais
    st.header('Tendências Temporais')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dados_completos['Tempo'], dados_completos['Pressao_entrada_bar'], label='Pressão de Entrada (bar)')
    ax.plot(dados_completos['Tempo'], dados_completos['Pressao_saida_bar'], label='Pressão de Saída (bar)')
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Pressão (bar)')
    ax.set_title('Tendências Temporais da Pressão')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Dicionário para mapear as opções do menu com as funções correspondentes
paginas = {
    "Página 1": exibicao,
    "Página 2": analise,
}

st.markdown(
    """
    <style>
    .css-1dv1kvn {
        font-family: Arial, sans-serif;
    }

    .stButton > button {
        width: 100%;
        background-color: #414246;
        border: none;
        color: white;
        padding: 10px;
        cursor: pointer;
        font-size: 18px;
    }
    .stButton > button:hover {
        background-color: #12121C;
        color: #FF4B4B;
    }
    .stButton > button:focus {
        outline: none;
    }
    .stButton > button:active {
        background-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True
)

# Inicializa o estado da página
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Página 1'

# Barra lateral com botões para cada página
st.sidebar.title("Menu")
if st.sidebar.button('Exibição de Dados'):
    st.session_state.pagina = 'Página 1'
if st.sidebar.button('Análise de Dados'):
    st.session_state.pagina = 'Página 2'

# Chama a função correspondente à página selecionada
pagina = st.session_state.pagina
if pagina == 'Página 1':
    dados_pressao, dados_volume = exibicao()
elif pagina == 'Página 2':
    if 'dados_pressao' not in st.session_state or 'dados_volume' not in st.session_state:
        dados_pressao, dados_volume = exibicao()
        st.session_state['dados_pressao'] = dados_pressao
        st.session_state['dados_volume'] = dados_volume
    else:
        dados_pressao = st.session_state['dados_pressao']
        dados_volume = st.session_state['dados_volume']
    analise(dados_pressao, dados_volume)
