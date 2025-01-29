import time

import streamlit as st
from streamlit_cookies_controller import CookieController

st.set_page_config(page_title="Postlab", page_icon=':material/experiment:', layout="wide")

pages = {
    "Youtube": [
        #st.Page("home.py", title="Bem-vindo ao Postlab!", default=True, icon=":material/experiment:"),
        st.Page("youtube/selecionar_conteudo.py", title="Escolher Vídeos", icon=":material/video_search:"),
        st.Page("youtube/criar_artigos.py", title="Criar Artigos", icon=":material/draw:"),
        st.Page("youtube/publicar_artigos.py", title="Publicar em massa", icon=":material/hub:"),
    ],
    "Rascunho": [
        #st.Page("rascunho/stepper_exemplo.py", title="Rascunho", icon=":material/drafts:"),
        #st.Page("rascunho/abas.py", title="Abas", icon=":material/drafts:"),
        #st.Page("rascunho/exemplo_busca.py", title="Exemplo Bsuca", icon=":material/drafts:"),
    ],
}

pg = st.navigation(pages)
pg.run()




with st.sidebar:
    st.markdown("""🗝️ **Api Keys**  
     :gray[É necessário configurar as API Keys abaixo]""")
    st.write("")

    cookie_controller = CookieController()

    youtube_api_key = st.text_input("Api Key Youtube:", type="password", value=cookie_controller.get("youtube_api_key"))

    if st.button("Salvar Configurações", use_container_width=True):
        cookie_controller.set('youtube_api_key', youtube_api_key)
        st.success("Configurações salvas com sucesso!")
        time.sleep(1)
        st.rerun()

    if st.button("Remover Configurações", use_container_width=True):
        cookie_controller.remove('youtube_api_key')
        st.success("Configurações removidas com sucesso!")
        time.sleep(1)
        st.rerun()





