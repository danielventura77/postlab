import streamlit as st

# Definindo os tópicos e seus códigos correspondentes
topicos = {
    "Música (tema principal)": "/m/04rlf",
    "Filmes": "/m/02vxn",
    "Esportes": "/m/06ntj",
    "Tecnologia": "/m/07c1v",
    "Ciência": "/m/01q6r",
    "Arte": "/m/0jjw"
}

# Inicializando o session_state para armazenar a seleção
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None

# Função para atualizar o session_state com a seleção
def update_selection(topic, code):
    st.session_state.selected_topic = code
    st.write(f"Você selecionou: {topic} com o código: {code}")

# Layout da aplicação
st.title("Seletor de Tópicos")

# Dividindo os tópicos em cards
for topic, code in topicos.items():
    with st.container():
        st.markdown(f"### {topic}")
        if st.button(f"Selecionar {topic}", key=code):
            update_selection(topic, code)

# Exibindo a seleção atual
if st.session_state.selected_topic:
    st.write(f"Tópico selecionado: {st.session_state.selected_topic}")
else:
    st.write("Nenhum tópico selecionado.")