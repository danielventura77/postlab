import googleapiclient.discovery

def busca_categorias_api(api_key):
    # Cria o serviço da API do YouTube
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Faz a requisição para obter as categorias de vídeo
    request = youtube.videoCategories().list(
      part="snippet",
      regionCode="US"  # Você pode mudar o código de região conforme necessário
    )
    response = request.execute()

    # Extrair as categorias e criar um dicionário {label: id}
    categs = {item["snippet"]["title"]: item["id"] for item in response["items"]}
    categs = {"Todas": None, **categs}
    return categs

