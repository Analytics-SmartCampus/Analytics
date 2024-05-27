import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

st.title('Teste de grafico e manipulação')

### GRÁFICO DE CAIXA D'AGUA------------------------------------------------

#Parâmetros
intervalo_minutos = st.slider('Dados registrados a cada minuto',
          min_value=15,
          max_value=30,
          value=15)
num_dias = st.slider('Quantidade de dias de registros',
          min_value=1,
          max_value=7,
          value=1)
nivel_inicial = 1000
variacao_maxima = 10

#Calculo de pontos
num_pontos = (24 * 60 // intervalo_minutos) * num_dias

#Gerar tempos
tempos = pd.date_range(start='2024-01-01 00:00:00', periods=num_pontos, freq=f'{intervalo_minutos}T')

#Nível de água
np.random.seed(42)
variacoes = np.random.randint(-variacao_maxima, variacao_maxima + 1, size=num_pontos)
niveis = nivel_inicial + np.cumsum(variacoes)

#DataFrame
dados = pd.DataFrame({'Tempo': tempos, 'Nivel_agua_mm': niveis})

#Exibir os dados no Streamlit
st.write(dados)

# Plotar o gráfico
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dados['Tempo'], dados['Nivel_agua_mm'], marker='o', linestyle='-', color='b')
ax.set_xlabel('Tempo')
ax.set_ylabel('Nível de Água (mm)')
ax.set_title('Nível de Água do Tanque a Cada 15 Minutos')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir o gráfico no Streamlit
st.pyplot(fig)

###
st.markdown('---')
###

### GRÁFICO DO HIDROMETRO------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Parâmetros da simulação
intervalo_minutos = st.slider('Minutos',min_value=15,max_value=30)  # Intervalo de tempo em minutos
num_dias = st.slider('Dias',min_value=1,max_value=7)  # Duração da simulação em dias

volume_inicial = 0  # Volume inicial em litros
consumo_maximo = 5  # Consumo máximo de água por intervalo em litros

# Calcular o número total de pontos de dados por dia
num_pontos_por_dia = 24 * 60 // intervalo_minutos

# Gerar os tempos
tempos = pd.date_range(start='2024-01-01 00:00:00', periods=num_pontos_por_dia * num_dias, freq=f'{intervalo_minutos}T')

# Gerar os dados de consumo de água
np.random.seed(42)  # Para reprodutibilidade
consumos = np.random.randint(0, consumo_maximo + 1, size=num_pontos_por_dia * num_dias)

# Calcular o volume acumulado com reset diário
volumes = []
for dia in range(num_dias):
    volume_diario = volume_inicial + np.cumsum(consumos[dia * num_pontos_por_dia:(dia + 1) * num_pontos_por_dia])
    volumes.extend(volume_diario)

# Criar o DataFrame
dados = pd.DataFrame({'Tempo': tempos, 'Volume_acumulado_L': volumes})

# Exibir os dados
st.write(dados)

# Plotar o gráfico
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dados['Tempo'], dados['Volume_acumulado_L'], marker='o', linestyle='-', color='b')
ax.set_xlabel('Tempo')
ax.set_ylabel('Volume Acumulado (L)')
ax.set_title('Volume Acumulado no Hidrômetro a Cada 15 Minutos')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

###
st.markdown('---')
###

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Parâmetros da simulação
intervalo_minutos = st.slider('Por Minuto',min_value=15,max_value=30)
num_dias = st.slider('Medida dos Dias',min_value=1,max_value=7)

pressao_entrada_inicial = 10  # Pressão inicial de entrada em bar
pressao_saida_inicial = 5  # Pressão inicial de saída em bar
variacao_pressao = 0.5  # Variação máxima de pressão por intervalo em bar

# Calcular o número total de pontos de dados por dia
num_pontos_por_dia = 24 * 60 // intervalo_minutos

# Gerar os tempos
tempos = pd.date_range(start='2024-01-01 00:00:00', periods=num_pontos_por_dia * num_dias, freq=f'{intervalo_minutos}T')

# Gerar os dados de pressão de entrada e saída
np.random.seed(42)  # Para reprodutibilidade
variacoes_entrada = np.random.uniform(-variacao_pressao, variacao_pressao, size=num_pontos_por_dia * num_dias)
variacoes_saida = np.random.uniform(-variacao_pressao, variacao_pressao, size=num_pontos_por_dia * num_dias)

# Calcular as pressões acumuladas com reset diário
pressao_entrada = []
pressao_saida = []
for dia in range(num_dias):
    entrada_diaria = pressao_entrada_inicial + np.cumsum(variacoes_entrada[dia * num_pontos_por_dia:(dia + 1) * num_pontos_por_dia])
    saida_diaria = pressao_saida_inicial + np.cumsum(variacoes_saida[dia * num_pontos_por_dia:(dia + 1) * num_pontos_por_dia])
    pressao_entrada.extend(entrada_diaria)
    pressao_saida.extend(saida_diaria)

# Criar o DataFrame
dados = pd.DataFrame({'Tempo': tempos, 'Pressao_entrada_bar': pressao_entrada, 'Pressao_saida_bar': pressao_saida})

# Exibir os dados
st.write(dados)

# Plotar o gráfico de pressão de entrada
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(dados['Tempo'], dados['Pressao_entrada_bar'], marker='o', linestyle='-', color='b', label='Pressão de Entrada')
ax1.set_xlabel('Tempo')
ax1.set_ylabel('Pressão de Entrada (bar)')
ax1.set_title('Pressão de Entrada no Poço Artesiano a Cada 15 Minutos')
ax1.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Plotar o gráfico de pressão de saída
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(dados['Tempo'], dados['Pressao_saida_bar'], marker='o', linestyle='-', color='r', label='Pressão de Saída')
ax2.set_xlabel('Tempo')
ax2.set_ylabel('Pressão de Saída (bar)')
ax2.set_title('Pressão de Saída no Poço Artesiano a Cada 15 Minutos')
ax2.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar os gráficos no Streamlit
st.pyplot(fig1)
st.pyplot(fig2)