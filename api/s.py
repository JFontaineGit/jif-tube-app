from googleapiclient.discovery import build
import rich 
import pandas as pd
import re 

api_key = "AIzaSyDhUFUrs5MbqkG_6RaRIWhIFWcyOEK8qhE"
"""
def obtener_info_video_model(video_id, api_key):
    # Crear cliente
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()

    # Verificamos que haya datos
    if not response['items']:
        print("No se encontró el video")
        return None, None

    video = response['items'][0]

    # ---------- Datos para el modelo ----------
    datos_modelo = {
        "view_count": int(video['statistics'].get('viewCount', 0)),
        "like_count": int(video['statistics'].get('likeCount', 0)),
        "comment_count": int(video['statistics'].get('commentCount', 0)),
        "duration": video['contentDetails'].get('duration', 'PT0M0S'),
        "published_at": video['snippet'].get('publishedAt', ''),
        "channel_title": video['snippet'].get('channelTitle', ''),
        "tags": video['snippet'].get('tags', [])
    }
    
    return datos_modelo
"""


def obtener_info_video_app(api_key, max_results=5):    
    # Crear cliente
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request para obtener videos populares
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        chart="mostPopular",
        
        maxResults=max_results,
        regionCode="US",  # Puedes cambiar la región si lo deseas
        videoCategoryId="10" # Music
    )
    response = request.execute()

    # Verificamos que haya datos
    if not response['items']:
        print("No se encontraron videos populares")
        return []

    videos_info = []

    for video in response['items']:
        datos_app = {
            "title": video['snippet'].get('title', ''),
            "thumbnail": video['snippet']['thumbnails']['high']['url'],
            "channel_title": video['snippet'].get('channelTitle', ''),
            "published_at": video['snippet'].get('publishedAt', ''),
            "duration": video['contentDetails'].get('duration', 'PT0M0S'),
            "view_count": int(video['statistics'].get('viewCount', 0)),
            "like_count": int(video['statistics'].get('likeCount', 0)),
        }
        videos_info.append(datos_app)
    
    return videos_info

# Ejemplo de uso
videos_populares = obtener_info_video_app(api_key, max_results=10)

df_app = pd.DataFrame(videos_populares)

#model = obtener_info_video_model("dQw4w9WgXcQ", api_key)


#rich.print(f"data: {model}")

#df_model = pd.DataFrame(model)

def convertir_duracion(duracion):
    match = re.match(r'PT(\d+M)?(\d+S)?', duracion)
    minutos = int(match.group(1)[:-1]) if match.group(1) else 0
    segundos = int(match.group(2)[:-1]) if match.group(2) else 0
    return f"{minutos}:{segundos:02d}"  # Formato M:SS

df_app['duration'] = df_app['duration'].apply(convertir_duracion)

print(df_app)