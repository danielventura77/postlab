import streamlit as st

# Inicializando valores no session_state
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "search_option" not in st.session_state:
    st.session_state["search_option"] = "Quero pesquisar no smart search do Postlab"
if "search_term" not in st.session_state:
    st.session_state["search_term"] = ""
if "channel_name" not in st.session_state:
    st.session_state["channel_name"] = ""
if "published_before" not in st.session_state:
    st.session_state["published_before"] = ""
if "published_after" not in st.session_state:
    st.session_state["published_after"] = ""
if "video_links" not in st.session_state:
    st.session_state["video_links"] = ""
if "preference" not in st.session_state:
    st.session_state["preference"] = "Option 1"

# Função para navegação entre os steps
def next_step():
    st.session_state.step += 1

def previous_step():
    st.session_state.step -= 1

# Step 1: Escolha dos vídeos
if st.session_state.step == 1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/YouTube_icon_%282013-2017%29.png/320px-YouTube_icon_%282013-2017%29.png", width=50)
    st.title("Youtube")
    st.subheader("Etapa 1 de 3: Quais vídeos? 🤔")

    search_option = st.radio(
        "Escolha como inputar os vídeos",
        ["Quero pesquisar no smart search do Postlab", "Já tenho os links dos vídeos"],
        key="search_option",
    )

    if search_option == "Quero pesquisar no smart search do Postlab":
        st.text_input("Termo de Pesquisa", key="search_term")
        st.text_input("Nome do Canal", key="channel_name")
        st.checkbox("Restringir apenas a Canais de Programas", key="restrict_to_program_channels")
        st.date_input("Publicado antes de", key="published_before")
        st.date_input("Publicado depois de", key="published_after")
    else:
        st.text_area("Informe os links dos vídeos", key="video_links")

    st.button("Próximo", on_click=next_step)

# Step 2: Preferências
elif st.session_state.step == 2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/YouTube_icon_%282013-2017%29.png/320px-YouTube_icon_%282013-2017%29.png", width=50)
    st.title("Youtube")
    st.progress(2 / 3)
    st.subheader("Step 2/3: Preferences")

    st.selectbox("Choose your preference:", ["Option 1", "Option 2", "Option 3"], key="preference")
    st.checkbox("I agree to the terms and conditions", key="terms")

    st.button("Anterior", on_click=previous_step)
    st.button("Próximo", on_click=next_step)

# Step 3: Confirmação
elif st.session_state.step == 3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/YouTube_icon_%282013-2017%29.png/320px-YouTube_icon_%282013-2017%29.png", width=50)
    st.title("Youtube")
    st.progress(3 / 3)
    st.subheader("Step 3/3: Confirm")

    st.write("**Opções selecionadas:**")
    st.write(f"- Método de Input: {st.session_state.search_option}")
    if st.session_state.search_option == "Quero pesquisar no smart search do Postlab":
        st.write(f"- Termo de Pesquisa: {st.session_state.search_term}")
        st.write(f"- Nome do Canal: {st.session_state.channel_name}")
        st.write(f"- Publicado antes de: {st.session_state.published_before}")
        st.write(f"- Publicado depois de: {st.session_state.published_after}")
    else:
        st.write(f"- Links dos vídeos: {st.session_state.video_links}")

    st.write(f"- Preferência: {st.session_state.preference}")

    st.button("Anterior", on_click=previous_step)
    st.button("Concluir")
