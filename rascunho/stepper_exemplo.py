import datetime
import streamlit as st
from streamlit import rerun, session_state

#Configurações da página
#st.set_page_config(page_title="Postlab", page_icon=':material/experiment:', layout="centered")

# Stepper
total_steps = 3
# Inicializar o estado da aplicação
if "step" not in st.session_state:
    st.session_state.step = 1

# Funções para mudar de etapa
def next_step():
    if st.session_state.step < total_steps:  # Exemplo: 3 etapas
        st.session_state.step += 1
        rerun()

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        rerun()

#Título
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("assets/images/youtube-logo.svg", width=85)
with col2:
    st.title("Youtube")


#Barra de Progresso do Stepper
progress = (st.session_state.step - 1) / (total_steps - 1)
st.progress(progress)  # Atualiza a barra de progresso (0 a 1)


def monta_campos_filtro():
    st.text_input("**Termo de Pesquisa**", value=st.session_state.get("termo_pesquisa", None), key="termo_pesquisa")

    st.text_input("**Nome do Canal**", value=st.session_state.get("nome_canal", None), key="nome_canal")
    st.toggle("Restringir apenas a Canais de Programas", value=st.session_state.get("canais_de_programa", None), key="canais_de_programa")

    cln1, cln2, cln3, cln4 = st.columns([3, 2, 3, 2], vertical_alignment="bottom")
    with cln1:
        st.date_input("**Publicado antes de**", value=st.session_state.get("publicado_antes_de", None),
                                                            format="DD/MM/YYYY", key="publicado_antes_de")
    with cln2:
        st.time_input(label="time1", value=st.session_state.get("publicado_antes_de_time",
                                                                    datetime.time(0, 0)),
                                                                 label_visibility="collapsed", key="publicado_antes_de_time")

    with cln3:
        st.date_input("**Publicado depois de**", value=st.session_state.get("publicado_depois_de", None),
                                                             format="DD/MM/YYYY", key="publicado_depois_de")
    with cln4:
        st.time_input(label="time2",
                                                                   value=st.session_state.get(
                                                                       "publicacao_depois_de_time",
                                                                       datetime.time(0, 0)),
                                                                   label_visibility="collapsed", key="publicacao_depois_de_time")



def etapa_selecao_videos(titulo):


    st.subheader(f"Etapa {st.session_state.step} de {total_steps}: {titulo}")

    st.write("")

    opcoes = [
        ":rainbow[**Quero pesquisar no smart search do Postlab**]",
        "**Já tenho os links dos vídeos**"
    ]

    if "filtrar_videos" not in st.session_state:
        st.session_state["filtrar_videos"] = opcoes[0]

    st.radio(
        "Escolha como inputar os vídeos",
        opcoes,
        captions=[
            "Necessita chave de API do youtube configurada",
            "Você informará os links dos vídeos diretamente"
        ], horizontal=True, key="filtrar_videos", index=0 if st.session_state["filtrar_videos"] == opcoes[0] or None else 1)

    st.write("")


    # Implementação das ações
    if st.session_state.get("filtrar_videos") == opcoes[0]:
        monta_campos_filtro()

    else:
        st.text_area("Informe os links dos vídeos", value=st.session_state.get("videos_selecionados", None),
                     key="videos_selecionados")




if st.session_state.step == 1:
    etapa_selecao_videos("Quais vídeos? 🤔")

elif st.session_state.step == 2:
    st.subheader(f"Step {st.session_state.step}/{total_steps}: Preferences")
    st.session_state.preference = st.selectbox("Choose your preference:", ["Option 1", "Option 2", "Option 3"])
    st.session_state.agree = st.checkbox("I agree to the terms and conditions")

elif st.session_state.step == 3:
    st.write("")

# Navegação
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    if st.session_state.step!=1 and st.button("Anterior" ,use_container_width=True, icon=':material/arrow_back:'):
        prev_step()
with col3:
    if st.button("Próximo", use_container_width=True, icon=':material/arrow_forward:'):
        next_step()

st.write(st.session_state)





