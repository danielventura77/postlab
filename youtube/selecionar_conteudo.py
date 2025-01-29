import streamlit as st
import folium
from streamlit_cookies_controller import CookieController
from streamlit_folium import st_folium

from backend.busca_youtube import search
from colecoes.categorias import busca_categorias
from colecoes.idiomas import idiomas_iso
from colecoes.paises import paises_iso
from colecoes.topicos import lista_topicos

#Título
titleCol1, titleCol2 = st.columns([0.05, 0.95])
with titleCol1:
    st.image("assets/images/youtube-logo.svg", width=85)
with titleCol2:
    st.header("Youtube", divider="rainbow")

st.write("")

def monta_mapa():
    # Cria um mapa centrado em uma localização inicial
    m = folium.Map(location=[-23.5505, -46.6333], zoom_start=10)

    # Adiciona a funcionalidade de desenhar um círculo no mapa
    draw = folium.plugins.Draw(
        draw_options={
            "circle": True,
            "circlemarker": False,
            "marker": False,
            "polygon": False,
            "polyline": False,
            "rectangle": False,
        },
        edit_options={
            "edit": False  # Desabilita a edição de formas
        }
    )
    m.add_child(draw)

    # Exibe o mapa no Streamlit
    map_data = st_folium(m, width=700, height=500, key=None)

    # Verifica se um círculo foi desenhado
    if map_data.get("last_active_drawing"):
        circle_data = map_data["last_active_drawing"]["geometry"]
        center = circle_data["coordinates"][::-1]  # Inverte para obter [lat, lon]
        radius_meters = map_data["last_active_drawing"]["properties"]["radius"]

        # Converte o raio de metros para quilômetros
        radius_km = radius_meters / 1000

        # Salva os dados no session_state
        if map_data.get("all_drawings"):
            st.session_state.location = center
            st.session_state.locationRadius = radius_km
        else:
            st.session_state.location = None
            st.session_state.locationRadius = None


def monta_resultado(itens):
    st.markdown("##### Resultados")
    for item in itens:

        # Incorpora o vídeo do YouTube usando iframe
        st.markdown(
            f'<iframe width="100%" height="400" src="https://www.youtube.com/embed/{item["video_id"]}" frameborder="0" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
            f'picture-in-picture" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )

        # Exibe os detalhes do vídeo
        st.subheader(f'{item["title"]}')
        col1, col2 = st.columns(2)
        with col1:
            st.page_link(f'https://www.youtube.com/channel/{item["channel_id"]}', label=f':green[{item["channel_title"]}]')
        with col2:
            st.write(f'Publicado em :green[{item["published_at"].strftime("%d/%m/%Y %H:%M:%S")}]')

        st.write(f':grey[{item["description"]}]')

        st.write("---")



mainCol1, mainCol2 = st.columns([0.34, 0.67], border=True)
with mainCol1:

    # Criando abas
    aba1, aba2 = st.tabs([":rainbow[**Quero Pesquisar via API do Youtube**]", "Já tenho os links dos vídeos"])
    with aba1:

        st.write("")
        direita, esquerda = st.columns(2, vertical_alignment="bottom")
        with direita:
            st.text_input("**🔎 Termo de Pesquisa**", value=st.session_state.get("termo_pesquisa", None),
                          key="q", help=""":orange[Para pesquisar vídeos que correspondam a :blue[**"remo" ou "vela"**],   
                                                   defina o termo de busca como :blue[**remo|vela**]. Da mesma forma, para pesquisar  
                                                   vídeos correspondentes a :blue[**"remo" ou "vela", mas não "pesca"**], defina o  
                                                   termo de busca como :blue[**remo|vela -pesca.**]  
                                                    Selecione ao lado os tipos de resultado: video, playlist e channel]""")
        with esquerda:
            selectionType = st.pills("**Tipo da busca**", ["video", "playlist", "channel"],
                                 selection_mode="multi", label_visibility="visible", default="video")
            st.session_state.type = ",".join(selectionType)


        st.toggle("Restringir apenas a Canais de Programas", value=st.session_state.get("channelType", None),
                  key="channelType", help=""":orange[Um exemplo de canal de programas no YouTube  
                                                    seria o canal oficial de uma produtora de séries,  
                                                    como o :blue[**Netflix, HBO Max Brasil, Discovery  
                                                    Channel Brasil ou Porta dos Fundos.**] Esses  
                                                    canais frequentemente organizam seu conteúdo em  
                                                    playlists temáticas baseadas em suas séries ou  
                                                    programas de TV.]""")

        cl1, cl2 = st.columns(2, vertical_alignment="bottom")
        with cl1:
            st.date_input("**Publicado depois de**", value=st.session_state.get("publishedAfter", None),
                      format="DD/MM/YYYY", key="publishedAfter")
        with cl2:
            st.date_input("**Publicado antes de**", value=st.session_state.get("publishedBefore", None),
                      format="DD/MM/YYYY", key="publishedBefore")

        colEsq, colDir = st.columns(2, vertical_alignment="bottom")
        with colEsq:
            st.selectbox("Busca Segura", ("none", "moderate", "strict"), key="safeSearch", index=0,
                         placeholder="Selecione",
                         help=""":orange[:blue[**none:**] Não restringe conteúdo sensível para um contexto familiar, educacional ou corporativo.  
                         :blue[**moderate:**] Aplica filtragem moderada.  
                         :blue[**strict:**] Aplica filtragem restritiva permitindo somente conteúdo apropriado para todas as audiências.]""")

            idiomas_iso = {"Todos": None, **idiomas_iso}
            idioma_selecionado = st.selectbox("Idioma", list(idiomas_iso.keys()),
                                            help=""":orange[Restringe a pesquisa incluindo relevância  
                                                para um determinado idioma]""")

            st.session_state.relevanceLanguage = idiomas_iso[idioma_selecionado]

        with colDir:

            paises_iso = {"Todos": None, **paises_iso}
            pais_selecionado = st.selectbox("País", list(paises_iso.keys()),
                                            help=""":orange[Restringe a pesquisa somente a vídeos que  
                                            podem ser assistidos no país especificado]""")

            st.session_state.regionCode = paises_iso[pais_selecionado]

            st.selectbox("Ordenação", ("date", "rating", "relevance", "title", "videoCount", "viewCount"), key="order", index=0,
                         placeholder="Selecione",
                         help=""":orange[:blue[**date:**] Com base na data em que foram criados, do mais recente para o mais antigo.  
                         :blue[**rating:**] Maior para a menor classificação.  
                         :blue[**relevance:**] Com base na relevância.  
                         :blue[**title:**] ordem alfabética por título.    
                         :blue[**videoCount:**] Os canais são classificados em ordem decrescente do número de vídeos enviados.  
                         :blue[**viewCount:**] Os recursos são classificados do maior para o menor número de visualizações.  
                                               Nas transmissões ao vivo, os vídeos são classificados pelo número de espectadores  
                                               simultâneos enquanto as transmissões estão em andamento.
                         ]""")

        st.write("")

        exp_estatisticas = st.expander("📈 **Filtrar por Estatísticas do Vídeo**")
        with exp_estatisticas:
            st.write("")
            left, right = st.columns(2, vertical_alignment="bottom")
            with left:
                st.text_input("A partir de quantas visualizações?", key="viewCountVideo")
                st.text_input("A partir de quantos comentários?", key="commentCount")
            with right:
                st.text_input("A partir de quantas curtidas?", key="likeCount")
                st.text_input("A partir de quantas favoritadas?", key="favoriteCount")

            # Validação dos campos
            if (st.session_state.viewCountVideo and not st.session_state.viewCountVideo.isdigit()) or \
                    (st.session_state.commentCount and not st.session_state.commentCount.isdigit()) or \
                    (st.session_state.likeCount and not st.session_state.likeCount.isdigit()) or \
                    (st.session_state.favoriteCount and not st.session_state.favoriteCount.isdigit()):
                st.error("Digite apenas números!")


        exp_estat_video = st.expander("📊 **Filtrar por Estatísticas do Canal**")
        with exp_estat_video:
            st.write("")
            st.text_input("A partir de quantos inscritos?", key="subscriberCount")
            left, right = st.columns(2, vertical_alignment="bottom")
            with left:
                st.text_input("A partir de quantas visualizações totais do canal?", key="viewCountChannel")

            with right:
                st.text_input("A partir de quantos vídeos publicados?", key="videoCountChannel")

            # Validação dos campos
            if (st.session_state.subscriberCount and not st.session_state.subscriberCount.isdigit()) or \
                    (st.session_state.viewCountChannel and not st.session_state.viewCountChannel.isdigit()) or \
                    (st.session_state.videoCountChannel and not st.session_state.videoCountChannel.isdigit()):
                st.error("Digite apenas números!")


        if "video" in selectionType:
            exp_video = st.expander("📺 **Filtrar por Atributos do Vídeo**")
            with exp_video:
                st.write("")
                cln1, cln2 = st.columns(2, vertical_alignment="bottom")
                with cln1:

                        st.selectbox("Tipo do Vídeo", ("any", "episode", "movie"), key="videoType", index=0,
                                     placeholder="Selecione",
                                     help=""":orange[:blue[**episode:**] Recupera apenas episódios de programas.  
                                     :blue[**movie:**] Recupera apenas filmes.]""")

                        st.selectbox("Duração do vídeo", ("any", "long", "medium", "short"), key="videoDuration", index=0,
                                     placeholder="Selecione",
                                     help=""":orange[:blue[**long:**] Vídeos com mais de 20 minutos.  
                                     :blue[**medium:**] Vídeos entre 4 e 20 minutos de duração.  
                                     :blue[**short:**] Vídeos com menos de quatro minutos de duração.]""")

                        st.selectbox("Vídeos Syndicated", ("any", "true"), key="videoSyndicated", index=0,
                                     placeholder="Selecione",
                                     help=""":orange[Filtra vídeos com base na permissão para serem  
                                                    reproduzidos em plataformas externas (syndication),  
                                                    como em dispositivos móveis ou outros aplicativos externos.  
                                                    :blue[**true:**] Vídeos que permitem syndication.]""")

                        st.selectbox("Conteúdo Patrocinado", ("any", "true"), key="videoPaidProductPlacement", index=0,
                                     placeholder="Selecione",
                                     help=""":orange[Filtra vídeos com base em conteúdo patrocinado.  
                                                    :blue[**true:**] Recupera apenas vídeos com patrocínio.]""")

                        st.selectbox("Legenda", ("any", "closedCaption", "none"), key="videoCaption", index=0,
                                     placeholder="Selecione",
                                     help=""":orange[:blue[**closedCaption:**] Inclui apenas vídeos com legendas.  
                                     :blue[**none:**] Inclui apenas os vídeos que não têm legendas.]""")

                with cln2:

                    st.selectbox("Tipo do Evento", ("any", "completed", "live", "upcoming"), key="eventType", index=0,
                                 placeholder="Selecione",
                                 help=""":orange[:blue[**completed:**] Inclui apenas transmissões concluídas.  
                                 :blue[**live:**] Inclui apenas transmissões ativas.  
                                 :blue[**upcoming:**] Inclui apenas as próximas transmissões.]""")


                    st.selectbox("Vídeos Incorporáveis (embedded)", ("any", "true"), key="videoEmbeddable", index=0,
                                 placeholder="Selecione",
                                 help=""":orange[Filtra vídeos com base na permissão para serem  
                                  incorporados (embedded) em outros sites ou aplicativos.  
                                  :blue[**true:**] Vídeos que permitem embedded.]""")

                    st.selectbox("Licença", ("any", "creativeCommon", "youtube"), key="videoLicense", index=0,
                                 placeholder="Selecione",
                                 help=""":orange[Filtra vídeos com base na Licença  
                                  :blue[**creativeCommon:**] Licença onde os vídeos podem ser reutilizados em outros vídeos.  
                                  :blue[**youtube:**] Retorna apenas os vídeos com a licença padrão do YouTube.]""")


                    st.selectbox("Definição", ("any", "high", "standard"), key="videoDefinition", index=0,
                                 placeholder="Selecione",
                                 help=""":orange[:blue[**high:**] Recupera apenas vídeos em HD.  
                                 :blue[**standard:**] Recupera apenas vídeos em definição padrão.]""")

                    st.selectbox("Dimensão", ("any", "2d", "3d"), key="videoDimension", index=0,
                                 placeholder="Selecione",
                                 help=""":orange[:blue[**2d:**] Exclui vídeos em 3d  
                                 :blue[**3d:**] Recupera somente vídeos em 3d.]""")

                categories = busca_categorias()
                selected_label = st.selectbox("Categoria", list(categories.keys()),
                                              label_visibility="visible",
                                              help=""":orange[Categorias são mais específicas e assertivas do que Tópicos]""")

                # Obter o id correspondente à label selecionada
                st.session_state.videoCategoryId = categories[selected_label]


        exp_topics = st.expander("🗂️ **Filtrar por Tópicos**")
        with exp_topics:
            st.markdown(""":gray[Os Tópicos são mais abrangentes que as Categorias, sendo assim, um Tópico pode englobar várias Categorias.]""")
            st.write("")
            topic_label = st.pills(
                "Tópicos", list(lista_topicos.keys()), label_visibility= "collapsed"
            )
            st.session_state.topicId = lista_topicos.get(topic_label, None)



        if "video" in selectionType:
            exp_loc_geo = st.expander("**🌐 Filtrar por Localização Geográfica**")
            with exp_loc_geo:
                st.markdown(""":gray[Use a barra de ferramentas de desenho para fazer um único círculo no mapa e restringir 
                 a busca somente a vídeos da área circunscrita. Em caso de mais de 1 círculo só será considerado o último.  
                 Vídeos que não especificam a localização geográfica nos metadados não serão listados]""")
                monta_mapa()

        st.write("")

        if st.button("🔎 Pesquisar", use_container_width=True):
            cookie_controller = CookieController()
            itens_result = search(cookie_controller.get("youtube_api_key"))
            with mainCol2:
                monta_resultado(itens_result)





    with aba2:

        st.write("")

        st.text_area("Informe os links dos vídeos separados por Enter", value=st.session_state.get("url_videos", None),
                     key="url_videos")




with mainCol2:
    st.empty()





