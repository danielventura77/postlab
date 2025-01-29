from datetime import datetime
import streamlit as st
from googleapiclient.discovery import build


# Buscar vídeos
def search(youtube_api_key):

    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    response = youtube.search().list(
        q=st.session_state.q,
        part='snippet',
        maxResults=50,
        type=st.session_state.type
    ).execute()

    itens = []
    for search_result in response.get('items', []):
        item = {
            'type': search_result['id']['kind'],
            'title': search_result['snippet']['title'],
            'description': search_result['snippet']['description'],
            'channel_title': search_result['snippet']['channelTitle'],
            'channel_id': search_result['snippet']['channelId'],
            'published_at': datetime.strptime(search_result['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
            'thumbnail': search_result['snippet']['thumbnails']['medium']['url'],
            'video_id': search_result['id']['videoId']
        }
        itens.append(item)
    return itens



