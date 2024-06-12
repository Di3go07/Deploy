import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

##BANCO DE DADOS

data = pd.read_csv(r'./Dados_F1/driver_standings.csv', sep=',')
data_driver_details = pd.read_csv(r'./Dados_F1/driver_details.csv', sep=',')
data_constructor_standings = pd.read_csv(r'./Dados_F1/constructor_standings.csv', sep=',')
data_races = pd.read_csv(r'./Dados_F1/race_summaries.csv', sep=',') 


##ESTRUTURA
st.set_page_config(
    layout="wide",
    page_title="TEMPORADAS F1", 
    page_icon=":checkered_flag:"
)
col1, col2 = st.columns(2, gap='large')

##CSS
with open("./DESAFIO_PYTHON/style.css", encoding="utf8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

##FILTRAR TEMPORADA
lista_temporadas = data['Year'].unique()
#salva uma lista com o ano de cada temporada


##TEXTO I SIDEBAR 
with st.container():
    st.sidebar.header(''':red[FORMULA 1] Dashboard''')
    st.sidebar.subheader('''1950 - 2022''')
st.sidebar.divider()


##BOTÃO TEMPORADA
temporada_escolhida = st.sidebar.selectbox("Temporada", lista_temporadas)
#seleciona a temporada a ser analisada


##FILTRAR PILOTOS
def filtrar_lista_pilotos():
    filtrar_pltLs = data_driver_details.query(f'Year == {temporada_escolhida}')
    return filtrar_pltLs
lista_dos_pilotos = filtrar_lista_pilotos()
#filtra a lista de pilotos na temporada

lista_pilotos = sorted(lista_dos_pilotos['Driver'].unique())
#salva a filtragem anterior

piloto_escolhido = st.sidebar.selectbox("Piloto", lista_pilotos, placeholder="Selecione um piloto")
#botão para selecionar o piloto da lista a ser analisado


##BOTÃO PILOTOS E CONSTRUTORAS
filtragem_PC = st.sidebar.radio('Selecione a filtragem',("Pilotos", "Construtoras"))
#seleciona se deseja ver a pontuação por piloto ou construtores

##TEXTO II SIDERBAR
st.sidebar.divider()
with st.container():
    st.sidebar.write("**Sobre**")
    st.sidebar.markdown("Diego Penna Andrade Barros")
    st.sidebar.markdown("PDITA 274")

##FUNÇÃO
def filtrar_ano():
    filtragem = data.query(f'Year == {temporada_escolhida}')
    return filtragem
tabela_ano = filtrar_ano()
#retorna a filtragem com as informações referentes ao ano escolhido

def filtrar_construtoras_ano():
    filtragem_constr = data_constructor_standings.query(f'Year == {temporada_escolhida}')
    return filtragem_constr
construtora_ano = filtrar_construtoras_ano()
#retorna detalhes das construras no ano escolhido
#DETALHE: as construtoras só começaram no ano de 1958, por isso antes desse ano  o gráfico está vazio

def filtrar_piloto_ano():
    filtragem_plt = data_driver_details.query(f'Year == {temporada_escolhida}')
    filtragem_plt = filtragem_plt.query(f'Driver == "{piloto_escolhido}"')
    return filtragem_plt
piloto_ano = filtrar_piloto_ano()
#retorna a filtagrem com o piloto escolhido na temporada 

def races_lap():
    filtragem_voltas = data_races.query(f'Year == {temporada_escolhida}')
    filtragem_voltas = filtragem_voltas['Time']
    return filtragem_voltas
tempo_voltas = races_lap()
#retorna a filtragem com o tempo da volta mais rapida em cada corrida da temporada


##GRÁFICOS
with col1:
    with st.container():
        st.image("DESAFIO_PYTHON/f1 _logo.png", width=150)
        st.title(f'Temporada de {temporada_escolhida}')
    with st.container():
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = len(data_races.query(f'Year == {temporada_escolhida}')),
            domain = {'x': [0, 1], 'y': [0, 1]},
            delta = {'reference': len(data_races.query(f'Year == 1950'))},
            title = {'text': "Número de corridas"},
            gauge = {'axis': {'range': [None, 25]},
                'steps' : [
                    {'range': [0, len(data_races)/72], 'color': "gray"}, #média do numero de corridas por temporada
                    {'range': [0, len(data_races.query(f'Year == 1950'))], 'color': "lightgray"}], #numero de corridas na primeira temporada
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': len(data_races.query(f'Year == 2022'))
                #numero de corridas na ultima temporada
            }}))
        col1.plotly_chart(fig)
    #cria um gráfico sobre as corridas na temporada

    with st.container():
        with st.expander('Legenda "Número de corridas"'):
            st.write('''**Barra cinza claro no fundo** representa a quantidade corridas na temporada de 1950''')
            st.write('''**Barra cinza no fundo** representa a média de corrida nas temporadas da Formula 1''')
            st.write('''**Barra laranja central** representa a quantidade corridas na temporada em análise''')
            st.write('''**Threshold**, o traço vermelho, representa o maior número de corridas já realizadas em uma temporada de Formula 1''')
            st.write('''**O número central** representa o número corridas na temporada em análise e o **delta**, o número abaixo, a comparação entre esse valor com o número de corridas realizadas na temporada de 1950''')
    #legenda do gráfico acima
    


    #metrics com a volta mais rapida e mais lenta de cada temporada

    with st.container():
        fig = px.line(piloto_ano, x="Grand Prix", y="PTS", hover_data=["Race Position"], title=(f'Desempenho {piloto_escolhido}'), width= 550, height= 500, markers=True, color_discrete_sequence =['lightblue'])
        col1.plotly_chart(fig)
    #cria um gráfico com a pontuação dos pilotos por corrida


with col2: 
    with st.container():
        st.subheader('PÓDIO DA TEMPORADA')
        col2_1, col2_2, col2_3 = st.columns(3)
        with col2_2:
            st.image('DESAFIO_PYTHON/piloto_icon.png', width=125)
            st.title('I º')
            st.write(tabela_ano['Driver'].iloc[0], '🏆')
            st.write(tabela_ano['PTS'].iloc[0], 'pontos')
        with col2_1:
            st.image('DESAFIO_PYTHON/piloto2_icon.png', width=100)
            st.title('2º')
            st.write(tabela_ano['Driver'].iloc[1]) 
            st.write(tabela_ano['PTS'].iloc[1], 'pontos')
        with col2_3:
            st.image('DESAFIO_PYTHON/piloto3_icon.png', width=125)
            st.title('3º')
            st.write(tabela_ano['Driver'].iloc[2]) 
            st.write(tabela_ano['PTS'].iloc[2], 'pontos')
 

    with st.container():
        if filtragem_PC == 'Construtoras':
            fig_date = px.pie(construtora_ano, values = 'PTS', names = 'Team', title='Pontuação no campeonato', width= 500, height= 550, color_discrete_sequence=px.colors.sequential.RdBu, labels='PTS')
            col2.plotly_chart(fig_date)
        if filtragem_PC == 'Pilotos':
            fig_date = px.bar(tabela_ano, y =  'Driver', x = 'PTS', hover_data=["Car","PTS"], title='Pontuação no campeonato', orientation="h", width= 500, height= 550, color_discrete_sequence =['red'])
            col2.plotly_chart(fig_date)  
    #cria um gráfico com a pontuação dos pilotos e construtores na temporada

    with st.container():
        with st.expander("DETALHE"):
            st.write('Nas temporadas de 1950 até 1957 não aparece o gráfico com a pontuação das construtoras, porque o campeonato das construtoras começou apenas em 1958')



