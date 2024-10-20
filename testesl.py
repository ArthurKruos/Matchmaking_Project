import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar a página para ter um layout amplo
st.set_page_config(layout="wide")

# Inicializando o DataFrame de usuários no session state se não existir
if 'users' not in st.session_state:
    st.session_state.users = pd.DataFrame({
        "Nome": ["Guri", "André Victor", "Kaio Victor", "Arthur Silva França"],
        "Idade": [19, 19, 20, 19],
        "Sexo": ["Masculino", "Feminino", "Indefinido", "Masculino"],
        "Gênero de jogo": ["Moba", "MOBA", "MOBA", "FPS"],
        "Jogo de busca": ["League of legends", "League of Legends", "Valorant", "Valorant"],
        "Nível ranked": ["Prata", "Ferro", "Não possui", "Imortal"],
        "Função": ["Top", "Top", "Smoke", "Duelista"],
        "Similaridade": [0.0] * 4  # Inicializando similaridade como 0
    })

# Função para adicionar um novo usuário
def cadastrar_user(nome, idade, sexo, genero_jogo, jogo_busca, nivel_ranked, funcao):
    novo_usuario = {
        "Nome": nome,
        "Idade": idade,
        "Sexo": sexo,
        "Gênero de jogo": genero_jogo,
        "Jogo de busca": jogo_busca,
        "Nível ranked": nivel_ranked,
        "Função": funcao,
        "Similaridade": 0.0  # Similaridade inicial como 0
    }
    novo_usuario = pd.DataFrame([novo_usuario])
    st.session_state.users = pd.concat([st.session_state.users, novo_usuario], ignore_index=True)

# Função para buscar um usuário
def buscar_user(nome):
    busca_resultado = st.session_state.users[st.session_state.users['Nome'].str.contains(nome, case=False, na=False)]
    return busca_resultado

# Função para encontrar um match (duo) baseado em similaridade
def encontrar_duo():
    if st.session_state.users.shape[0] < 2:
        return "Não há usuários suficientes para emparelhamento."
    users_sorted = st.session_state.users.sort_values(by="Similaridade", ascending=False)
    return users_sorted.iloc[1]

# Função de calculadora de similaridade
def calculadora_similaridade(user_new):
    # Manter todas as colunas necessárias para o cálculo
    users_array = st.session_state.users.copy()

    # Convertendo os dados de categóricos para maiúsculas para facilitar a comparação
    users_array['Gênero de jogo'] = users_array['Gênero de jogo'].str.upper()
    users_array['Jogo de busca'] = users_array['Jogo de busca'].str.upper()
    users_array['Nível ranked'] = users_array['Nível ranked'].str.upper()
    users_array['Função'] = users_array['Função'].str.upper()

    # Inicializando a lista de similaridade
    similaridade_resultados = []

    for idx, user in users_array.iterrows():
        if user['Nome'] == user_new['Nome']:  # Evitar comparar o novo usuário consigo mesmo
            continue
        
        # Calculando a similaridade
        similaridade = 0
        idade_diff = abs(user['Idade'] - user_new['Idade'])
        similaridade += (1 - idade_diff / 100) * 0.20  # Ajuste do peso da idade
        
        if user['Gênero de jogo'] == user_new['Gênero de jogo'].upper():
            similaridade += 0.20
        if user['Jogo de busca'] == user_new['Jogo de busca'].upper():
            similaridade += 0.20
        if user['Nível ranked'] == user_new['Nível ranked'].upper():
            similaridade += 0.20
        if user['Função'] == user_new['Função'].upper():
            similaridade += 0.20
        
        # Adicionando a similaridade ao usuário
        user_data = user.to_dict()  # Mantém todas as informações do usuário
        user_data['Similaridade'] = similaridade
        similaridade_resultados.append(user_data)

    # Criando um DataFrame a partir dos resultados
    resultados_df = pd.DataFrame(similaridade_resultados)
    return resultados_df

# Interface Streamlit
st.title("Sistema de Matchmaking de Jogos Online")

# Criar a lista de navegação com selectbox
menu_selection = st.sidebar.selectbox("Menu", ["Adicionar Usuário", "Buscar Usuário", "Encontrar DUO", "Mostrar Todos Usuários", "Informações do Projeto", "Matchmaking"])

# Navegação baseada na seleção do menu
if menu_selection == "Adicionar Usuário":
    st.header("Adicionar Novo Usuário")

    # Criação de 4 colunas para os campos
    col1, col2, col3, col4 = st.columns(4)  # Quatro colunas

    with col1:
        nome = st.text_input("Nome")
        genero_jogo = st.text_input("Gênero de jogo")

    with col2:
        idade = st.number_input("Idade", min_value=10, max_value=100)
        jogo_busca = st.text_input("Jogo de busca")

    with col3:
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Indefinido"])
        nivel_ranked = st.text_input("Nível ranked")

    with col4:
        funcao = st.text_input("Função")

    if st.button("Adicionar"):
        cadastrar_user(nome, idade, sexo, genero_jogo, jogo_busca, nivel_ranked, funcao)
        st.success(f"Usuário {nome} adicionado com sucesso!")

elif menu_selection == "Buscar Usuário":
    st.header("Buscar Usuário")
    nome_busca = st.text_input("Digite o nome do usuário que deseja buscar")
    if st.button("Buscar"):
        resultado = buscar_user(nome_busca)
        if not resultado.empty:
            st.write(f"Usuário encontrado: ")
            st.dataframe(resultado.style.set_table_attributes('style="width: 100%;"'), use_container_width=True)
        else:
            st.write("Usuário não encontrado.")

elif menu_selection == "Encontrar DUO":
    st.header("Encontrar DUO")
    duo = encontrar_duo()
    st.write(f"Match encontrado: {duo}")

elif menu_selection == "Mostrar Todos Usuários":
    st.header("Lista de Usuários Cadastrados")
    st.dataframe(st.session_state.users.style.set_table_attributes('style="width: 100%;"'), use_container_width=True)

elif menu_selection == "Informações do Projeto":
    st.header("Informações do Projeto de Matchmaking")
    st.write("""Este projeto visa facilitar a conexão entre jogadores de jogos online, permitindo que encontrem parceiros de jogo com características semelhantes e que compartilhem interesses em jogos específicos.

        **Funcionalidades do sistema:**
        - **Adicionar Usuário:** Permite que novos usuários sejam cadastrados no sistema.
        - **Buscar Usuário:** Facilita a busca de usuários cadastrados, permitindo que se encontre jogadores por nome.
        - **Encontrar DUO:** O sistema pode encontrar um par (duo) para jogar com base na similaridade dos jogadores.
        - **Mostrar Todos Usuários:** Exibe uma lista de todos os usuários cadastrados no sistema.

        **Objetivo do Projeto:**
        O objetivo é criar uma plataforma intuitiva e eficiente para unir jogadores, promovendo uma melhor experiência no jogo através da formação de duplas com interesses e habilidades compatíveis.

        **Referência do Código Fonte:**
        Você pode encontrar o código fonte do projeto no GitHub: [Matchmaking_Project](https://github.com/ArthurKruos/Matchmaking_Project)
    """)

    # Gráfico de Dispersão com Plotly
    st.subheader("Gráfico de Dispersão da Similaridade dos Usuários")
    if not st.session_state.users.empty:
        fig = px.scatter(st.session_state.users, x='Idade', y='Similaridade', 
                         text='Nome', title='Dispersão da Similaridade dos Usuários', 
                         labels={'Idade': 'Idade', 'Similaridade': 'Similaridade'},
                         color='Similaridade', color_continuous_scale='Viridis')
        st.plotly_chart(fig)

elif menu_selection == "Matchmaking":
    st.header("Executar Matchmaking")

    # Criação de 2 colunas para cadastrar o novo usuário para matchmaking
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cadastrar Novo Usuário para Matchmaking")
        nome = st.text_input("Nome")
        idade = st.number_input("Idade", min_value=10, max_value=100)
        genero_jogo = st.text_input("Gênero de jogo")
        jogo_busca = st.text_input("Jogo de busca")
        nivel_ranked = st.text_input("Nível ranked")
        funcao = st.text_input("Função")

        if st.button("Executar Matchmaking"):
            user_new = {
                'Nome': nome,
                'Idade': idade,
                'Gênero de jogo': genero_jogo,
                'Jogo de busca': jogo_busca,
                'Nível ranked': nivel_ranked,
                'Função': funcao,
            }
            resultados = calculadora_similaridade(user_new)
            if not resultados.empty:
                st.write("Usuários mais similares encontrados:")
                st.dataframe(resultados[['Nome', 'Idade', 'Gênero de jogo', 'Jogo de busca', 'Nível ranked', 'Função', 'Similaridade']].style.set_table_attributes('style="width: 100%;"'), use_container_width=True)
                # Gerar gráfico de dispersão
                fig = px.scatter(resultados, x='Idade', y='Similaridade', text='Nome', title='Similaridade dos Usuários', labels={'Idade': 'Idade', 'Similaridade': 'Similaridade'})
                st.plotly_chart(fig)  # Mostrando o gráfico
            else:
                st.write("Nenhum usuário encontrado para similaridade.")

    with col2:
        st.subheader("Usuários Cadastrados para Matchmaking")
        st.dataframe(st.session_state.users[['Nome', 'Idade', 'Gênero de jogo', 'Jogo de busca', 'Nível ranked', 'Função']].style.set_table_attributes('style="width: 100%;"'), use_container_width=True)
